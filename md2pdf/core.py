"""md2pdf core module."""
from pathlib import Path
from typing import Optional

from markdown2 import markdown, markdown_path
from weasyprint import CSS, HTML

from .exceptions import ValidationError


def md2pdf(
    pdf: Path,
    raw: Optional[str] = None,
    md: Optional[Path] = None,
    css: Optional[Path] = None,
    base_url: Optional[Path] = None,
):
    """Converts input markdown to styled HTML and renders it to a PDF file.

    Args:
        pdf: output PDF file path.
        md: input markdown file path.
        raw: input markdown raw string content.
        css: input styles path (CSS).
        base_url: absolute base path for markdown linked content (as images).

    Returns:
        None

    Raises:
        ValidationError: if md_content and md_file_path are empty.
    """
    # Convert markdown to html
    raw_html: str = ""
    extras: list = ["cuddled-lists", "tables", "footnotes"]
    if md:
        raw_html = markdown_path(md, extras=extras)
    elif raw:
        raw_html = markdown(raw, extras=extras)

    if not len(raw_html):
        raise ValidationError("Input markdown seems empty")

    # Weasyprint HTML object
    html: HTML = HTML(string=raw_html, base_url=str(base_url))

    # Get styles
    styles: list = []
    if css:
        styles.append(CSS(filename=css))

    # Generate PDF
    html.write_pdf(pdf, stylesheets=styles)
