# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from markdown2 import markdown, markdown_path
from weasyprint import HTML, CSS

from .exceptions import ValidationError


def md2pdf(pdf_file_path, md_content=None, md_file_path=None,
           css_file_path=None, base_url=None):
    """
    Converts input markdown to styled HTML and renders it to a PDF file.

    Args:
        pdf_file_path: output PDF file path.
        md_content: input markdown raw string content.
        md_file_path: input markdown file path.
        css_file_path: input styles path (CSS).
        base_url: absolute base path for markdown linked content (as images).

    Returns:
        None

    Raises:
        ValidationError: if md_content and md_file_path are empty.
    """

    # Convert markdown to html
    raw_html = ''
    extras = ['cuddled-lists', 'tables', 'footnotes']
    if md_file_path:
        raw_html = markdown_path(md_file_path, extras=extras)
    elif md_content:
        raw_html = markdown(md_content, extras=extras)

    if not len(raw_html):
        raise ValidationError('Input markdown seems empty')

    # Weasyprint HTML object
    html = HTML(string=raw_html, base_url=base_url)

    # Get styles
    css = []
    if css_file_path:
        css.append(CSS(filename=css_file_path))

    # Generate PDF
    html.write_pdf(pdf_file_path, stylesheets=css)

    return
