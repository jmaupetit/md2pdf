"""md2pdf CLI."""

import logging
from importlib.metadata import version
from pathlib import Path
from typing import Optional

import click

from .core import md2pdf

logger = logging.getLogger(__name__)


@click.command(name="md2pdf")
@click.argument("md", type=click.Path(exists=True))
@click.argument("pdf", type=click.Path())
@click.option("--css", "css", type=click.Path(exists=True))
@click.option("--extras", "-e", "extras", multiple=True, type=str)
@click.version_option(version=version("md2pdf"))
def cli(md: Path, pdf: Path, css: Optional[Path], extras: list):
    """md2pdf command line tool."""
    if css is not None:
        css = Path(css)
    md2pdf(Path(pdf), md=Path(md), css=css, base_url=Path.cwd(), extras=extras)
