"""md2pdf CLI."""
from importlib.metadata import version
from pathlib import Path

import click

from md2pdf.core import md2pdf


@click.command(name="md2pdf")
@click.argument("md_file_path", type=click.Path(exists=True))
@click.argument("pdf_file_path", type=click.Path())
@click.option("--css", "css_file_path", type=click.Path(exists=True))
@click.version_option(version=version("md2pdf"))
def cli(md_file_path, pdf_file_path, css_file_path):
    """md2pdf command line tool."""
    md2pdf(
        pdf_file_path,
        md_file_path=md_file_path,
        css_file_path=css_file_path,
        base_url=Path.cwd(),
    )
