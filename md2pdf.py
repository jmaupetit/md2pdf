#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from markdown2 import markdown_path
from weasyprint import HTML, CSS


def main(argv=None):

    # Convert markdown to html
    html = markdown_path('markdown-css-themes/sample.md')

    # Weasyprint HTML object
    html = HTML(string=html)

    # Get styles
    css = CSS(filename='markdown-css-themes/foghorn.css')

    # Generate PDF
    html.write_pdf('test.pdf', stylesheets=[css])

    return 1


if __name__ == '__main__':
    sys.exit(main())
