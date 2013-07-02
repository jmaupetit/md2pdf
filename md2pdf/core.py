# -*- coding: utf-8 -*-
from markdown2 import markdown_path
from weasyprint import HTML, CSS


def md2pdf(md_file_path, pdf_file_path, css_file_path=None):
    """
    Convert markdown file to pdf with styles
    """

    # Convert markdown to html
    raw_html = markdown_path(md_file_path, extras=["cuddled-lists"])

    # Weasyprint HTML object
    html = HTML(string=raw_html)

    # Get styles
    css = []
    if css_file_path:
        css.append(CSS(filename=css_file_path))

    # Generate PDF
    html.write_pdf(pdf_file_path, stylesheets=css)

    return
