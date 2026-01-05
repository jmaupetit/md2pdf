"""md2pdf - Markdown to PDF conversion tool.

Usage: md2pdf [options] INPUT.MD OUTPUT.PDF

Options:
    --css=STYLE.CSS
"""

from . import cli

if __name__ == "__main__":
    """Run the CLI."""
    cli.cli()
