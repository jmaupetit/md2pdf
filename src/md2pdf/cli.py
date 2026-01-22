"""md2pdf CLI."""

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version as metadata_version
from pathlib import Path
from time import time
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

from .core import md2pdf
from .exceptions import ValidationError

logger = logging.getLogger(__name__)

cli = typer.Typer(name="md2pdf", no_args_is_help=True, pretty_exceptions_short=True)
console = Console()


def parse_config(config: str) -> dict:
    """Parse configuration input as a JSON string."""
    try:
        parsed = json.loads(config)
    except json.decoder.JSONDecodeError as err:
        raise ValidationError(
            "Invalid input configuration string (should be valid JSON)"
        ) from err
    return parsed


@cli.command(no_args_is_help=True)
def main(
    md: Annotated[
        Optional[list[Path]],
        typer.Option(
            "--input",
            "-i",
            help="Markdown source file path (can be used multiple times).",
            exists=True,
        ),
    ] = None,
    pdf: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="PDF output file path (when a single md input is used).",
        ),
    ] = None,
    css: Annotated[
        Optional[Path], typer.Option("--css", "-c", help="Input CSS file.", exists=True)
    ] = None,
    extras: Annotated[
        Optional[list[str]],
        typer.Option(
            "--extras",
            "-e",
            help="Extra markdown extension to activate (cam be used multiple times).",
        ),
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option(
            "--config",
            "-C",
            help="Markdown extensions configuration (as a JSON string).",
        ),
    ] = None,
    workers: Annotated[
        int,
        typer.Option("--workers", "-W", help="Number of parallel workers to start."),
    ] = 4,
    version: Annotated[
        bool, typer.Option("--version", "-V", help="Display program version.")
    ] = False,
):
    """Markdown to PDF conversion tool with styles… and templates!"""
    if version:
        console.print(f"{metadata_version('md2pdf')}")
        raise typer.Exit()

    if md is None or not len(md):
        console.print("🤷‍♂️ No markdown input file. See `--help`")
        raise typer.Exit(code=2)

    if pdf is not None and len(md) > 1:
        console.print(
            "❌ PDF output option `[red]--output/-o[/red]`"
            " cannot be used with multiple input."
        )
        raise typer.Exit(code=2)

    if css is not None:
        console.print(f"💅 CSS file: [blue]{css}[/blue]")
        css = Path(css)

    if extras is not None:
        console.print(f"🔧 Extras: [blue]{extras}[/blue]")

    extras_config = None
    if config is not None:
        extras_config = parse_config(config)
        console.print(f"🔧 Configuration: [blue]{extras_config}[/blue]")

    progress = Progress(
        SpinnerColumn(finished_text="✅"),
        TextColumn(
            "Converting: [blue]{task.fields[md]}[/blue] "
            "→ [green]{task.fields[pdf]}[/green]"
        ),
        "·",
        TimeElapsedColumn(),
        console=console,
    )

    def wrapper(task: TaskID, md_: Path, pdf: Path):
        """A wrapper for md2pdf thread execution with task progress update."""
        progress.start_task(task)
        md2pdf(
            pdf,
            md=md_,
            css=css,
            base_url=Path.cwd(),
            extras=extras if extras else None,
            extras_config=extras_config,
        )
        progress.update(task, completed=True)

    started_at = time()
    with progress:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for md_ in md:
                if pdf is None:
                    pdf = md_.with_suffix(".pdf")
                task = progress.add_task(
                    "convert", md=md_, pdf=pdf, total=1, start=False
                )
                pool.submit(wrapper, task, md_, pdf)

    console.print(f"🚀 Output files generated in [blue]{(time() - started_at):.3f}s[/]")
