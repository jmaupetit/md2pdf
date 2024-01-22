"""md2pdf CLI."""
from importlib.metadata import version
from pathlib import Path

import click

from md2pdf.core import md2pdf


@click.command(name="md2pdf")
@click.argument("md", type=click.Path(exists=True))
@click.argument("pdf", type=click.Path())
@click.option("--css", "css", type=click.Path(exists=True))
@click.option("--extras", "-e", "extras", multiple=True, type=str)
@click.version_option(version=version("md2pdf"))
def cli(md, pdf, css, extras):
    """md2pdf command line tool."""
    md2pdf(
        pdf,
        md=md,
        css=css,
        base_url=Path.cwd(),
        extras=extras
    )
