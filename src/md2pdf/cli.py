"""md2pdf CLI."""

import json
import logging
from importlib.metadata import version
from pathlib import Path
from typing import Optional

import click

from .core import md2pdf
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


def parse_config(config: str) -> dict:
    """Parse configuration input as a JSON string."""
    try:
        parsed = json.loads(config)
    except json.decoder.JSONDecodeError as err:
        raise ValidationError(
            "Invalid input configuration string (should be valid JSON)"
        ) from err
    return parsed


@click.command(name="md2pdf")
@click.argument("md", type=click.Path(exists=True))
@click.argument("pdf", type=click.Path())
@click.option("--css", "-c", "css", type=click.Path(exists=True))
@click.option("--extras", "-e", "extras", multiple=True, type=str)
@click.option("--config", "-C", "config", type=str)
@click.version_option(version=version("md2pdf"))
def cli(
    md: Path,
    pdf: Path,
    css: Optional[Path] = None,
    extras: Optional[list] = None,
    config: Optional[str] = None,
):
    """Markdown to PDF conversion with styles!"""
    if css is not None:
        css = Path(css)

    extras_config = None
    if config is not None:
        extras_config = parse_config(config)

    md2pdf(
        Path(pdf),
        md=Path(md),
        css=css,
        base_url=Path.cwd(),
        # FIXME: click returns a tuple and not a list
        extras=list(extras) if extras else None,
        extras_config=extras_config,
    )
