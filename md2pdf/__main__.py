"""md2pdf - Markdown to PDF conversion tool.

Usage: md2pdf [options] INPUT.MD OUTPUT.PDF

Options:
    --css=STYLE.CSS
"""
import os
import sys
from importlib.metadata import version

from docopt import docopt

from md2pdf.core import md2pdf


def main(argv=None):
    """md2pdf main script."""
    __version__ = version("md2pdf")

    # Parse command line arguments
    arguments = docopt(
        __doc__,
        version=f"md2pdf {__version__}"
    )

    # Paths
    md_file_path = arguments.get('INPUT.MD')
    pdf_file_path = arguments.get('OUTPUT.PDF')
    css_file_path = arguments.get('--css', None)
    base_url = os.getcwd()

    md2pdf(pdf_file_path,
           md_file_path=md_file_path,
           css_file_path=css_file_path,
           base_url=base_url)

    return 0


if __name__ == '__main__':
    sys.exit(main())
