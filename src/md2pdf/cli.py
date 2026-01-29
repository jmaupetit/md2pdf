"""md2pdf CLI."""

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from importlib.metadata import version as metadata_version
from pathlib import Path
from time import time
from typing import Annotated, List, Optional

try:
    import typer
except ModuleNotFoundError as err:
    raise RuntimeError(
        "Missing dependency: to use the CLI, you should install the `cli` extra first: "
        "`pip install md2pdf[cli]`"
    ) from err
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)
from watchfiles import watch as wf_watch

from .conf import CLI_WATCH_FORCE_POOLING
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


def _run_with_progress(
    progress: Progress,
    task: TaskID,
    md_: Path,
    pdf: Path,
    css: Optional[Path] = None,
    extras: Optional[list[str]] = None,
    extras_config: Optional[dict] = None,
):
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


def _start_threads(
    progress: Progress,
    workers: int,
    md: List[Path],
    pdf: Optional[Path] = None,
    css: Optional[Path] = None,
    extras: Optional[list[str]] = None,
    extras_config: Optional[dict] = None,
):
    """Run convertion in threads with progress."""
    started_at = time()
    tasks = []
    with progress:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for md_ in md:
                pdf_ = md_.with_suffix(".pdf") if pdf is None else pdf
                task = progress.add_task(
                    "convert", md=md_, pdf=pdf_, total=1, start=False
                )
                pool.submit(
                    _run_with_progress,
                    progress,
                    task,
                    md_,
                    pdf_,
                    css,
                    extras,
                    extras_config,
                )
                tasks.append(task)

    console.print(f"🚀 Output files generated in [blue]{(time() - started_at):.3f}s[/]")

    # Clean tasks
    for task in tasks:
        progress.remove_task(task)


def _get_progress(console: Console) -> Progress:
    """Get rich progress component."""
    return Progress(
        SpinnerColumn(finished_text="✅"),
        TextColumn(
            "Converting: [blue]{task.fields[md]}[/blue] "
            "→ [green]{task.fields[pdf]}[/green]"
        ),
        "·",
        TimeElapsedColumn(),
        console=console,
    )


def watcher_callback():
    """Dummy watcher callback used for testing."""


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
    watch: Annotated[
        bool,
        typer.Option(
            "--watch", "-w", help="Automatically render PDF upon input file(s) changes."
        ),
    ] = False,
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

    # Run rendering and exit (if watch is not active)
    _start_threads(_get_progress(console), workers, md, pdf, css, extras, extras_config)
    if not watch:
        raise typer.Exit()

    # Watch changes in CSS and markdown files
    paths_to_watch = ([css] if css else []) + md
    console.print(
        f"👀 Looking for changes in: {[str(p) for p in paths_to_watch]} "
        "(CTRL+C to quit)"
    )
    for changes in wf_watch(
        *paths_to_watch,
        force_polling=CLI_WATCH_FORCE_POOLING,
    ):
        changed_files = {Path(change[1]) for change in changes}
        console.rule(str(datetime.now()), align="right")
        console.print(f"⚡️ Detected changes in: {list(map(str, changed_files))}")
        changed_md = list(changed_files & set(md))
        if css in changed_files:
            changed_md = md

        _start_threads(
            _get_progress(console), workers, changed_md, pdf, css, extras, extras_config
        )

        watcher_callback()
