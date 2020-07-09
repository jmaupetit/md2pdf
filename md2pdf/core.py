# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from markdown2 import markdown, markdown_path
from weasyprint import CSS

from .exceptions import ValidationError
from .pdfgenerator import PdfGenerator


def md2pdf(
    pdf_file_path,
    md_content=None,
    md_file_path=None,
    css_file_path=None,
    header_content=None,
    header_file_path=None,
    footer_content=None,
    footer_file_path=None,
    base_url=None,
):
    """
    Converts input markdown to styled HTML and renders it to a PDF file.

    Args:
        pdf_file_path: output PDF file path.
        md_content: input markdown raw string content.
        md_file_path: input markdown file path.
        css_file_path: input styles path (CSS).
        header_content: input HTML header raw string content.
        header_file_path: input HTML header file path.
        footer_content: input HTML footer raw string content.
        footer_file_path: input HTML footer file path.
        base_url: absolute base path for markdown linked content (as images).

    Returns:
        None

    Raises:
        ValidationError: if md_content and md_file_path are empty.
    """

    # Convert markdown to html
    raw_html = ''
    extras = ['cuddled-lists', 'tables']
    if md_file_path:
        raw_html = markdown_path(md_file_path, extras=extras)
    elif md_content:
        raw_html = markdown(md_content, extras=extras)

    # Include header and footer
    if header_file_path:
        with open(header_file_path) as header_file:
            raw_header = header_file.read()
    else:
        raw_header = header_content
    if footer_file_path:
        with open(footer_file_path) as footer_file:
            raw_footer = footer_file.read()
    else:
        raw_footer = footer_content

    if not len(raw_html):
        raise ValidationError('Input markdown seems empty')

    # Get styles
    css = []
    if css_file_path:
        css.append(CSS(filename=css_file_path))

    # PdfGenerator using Weasyprint
    pdf_generator = PdfGenerator(
        main_html=raw_html,
        header_html=raw_header,
        footer_html=raw_footer,
        base_url=base_url,
        stylesheets=css,
    )

    # Generate PDF
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(pdf_generator.render_pdf())

    return
