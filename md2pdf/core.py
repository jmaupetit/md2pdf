# -*- coding: utf-8 -*-
from markdown2 import markdown, markdown_path
from weasyprint import HTML, CSS

from .exceptions import ValidationError

def md2pdf(pdf_file_path, md_content=None, md_file_path=None,
           css_file_path=None):
    """
    Convert markdown file to pdf with styles
    """

    # Convert markdown to html
    raw_html = ""
    extras = ["cuddled-lists"]
    if md_file_path:
        raw_html = markdown_path(md_file_path, extras=extras)
    elif md_content:
        raw_html = markdown(md_file_path, extras=extras)

    if not len(raw_html):
        raise ValidationError('Input markdown seems empty')

    # Weasyprint HTML object
    html = HTML(string=raw_html)

    # Get styles
    css = []
    if css_file_path:
        css.append(CSS(filename=css_file_path))

    # Generate PDF
    html.write_pdf(pdf_file_path, stylesheets=css)

    return
