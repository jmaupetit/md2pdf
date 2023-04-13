#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""md2pdf - Markdown to PDF conversion tool.

Usage: md2pdf [options] INPUT.MD OUTPUT.PDF

Options:
    --css=STYLE.CSS
    --new-extras=extras1,extras2,extras2 (separated by comma)
"""
import os
import sys

from docopt import docopt
from md2pdf import md2pdf, __version__


def main(argv=None):

    # Parse command line arguments
    arguments = docopt(
        __doc__,
        version='md2pdf %s' % __version__
    )

    # Paths
    md_file_path = arguments.get('INPUT.MD')
    pdf_file_path = arguments.get('OUTPUT.PDF')
    css_file_path = arguments.get('--css', None)
    new_extras = arguments.get('--new-extras', None)
    base_url = os.getcwd()
    
    md2pdf(pdf_file_path,
           md_file_path=md_file_path,
           css_file_path=css_file_path,
           base_url=base_url,
           new_extras=new_extras,
           )

    return 0


if __name__ == '__main__':
    sys.exit(main())
