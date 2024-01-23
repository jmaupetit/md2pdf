"""md2pdf core module."""
import logging
from pathlib import Path
from typing import List, Optional

import frontmatter
from jinja2 import Template
from markdown import markdown
from weasyprint import CSS, HTML

from .conf import MARKDOWN_EXTRAS
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


def md2pdf(
    pdf: Path,
    raw: Optional[str] = None,
    md: Optional[Path] = None,
    css: Optional[Path] = None,
    base_url: Optional[Path] = None,
    extras: List[str] = MARKDOWN_EXTRAS,
):
    """Converts input markdown to styled HTML and renders it to a PDF file.

    Args:
        pdf: output PDF file path.
        md: input markdown file path.
        raw: input markdown raw string content.
        css: input styles path (CSS).
        base_url: absolute base path for markdown linked content (as images).
        extras: markdown extras to activate

    Returns:
        None

    Raises:
        ValidationError: if md_content and md_file_path are empty.
    """
    if md:
        logger.debug("Reading markdown content from file %s", md)
        raw = md.read_text()

    if raw is None or not len(raw):
        raise ValidationError("Input markdown seems empty")

    context: dict = {}
    # Check if markdown file is a template
    if frontmatter.checks(raw):
        logger.info("Markdown input file contains frontmatter header")

        # Get context and the template
        context, template = frontmatter.parse(raw)
        logger.debug("Frontmatter context %s", context)

        # Render the template
        raw = Template(template).render(context)

    raw_html = markdown(raw, extensions=extras)

    # Weasyprint HTML object
    if base_url is None:
        base_url = Path.cwd()
    html: HTML = HTML(string=raw_html, base_url=str(base_url))

    # Get styles
    styles: list = []
    if css:
        styles.append(CSS(filename=css))

    # Generate PDF
    html.write_pdf(pdf, stylesheets=styles)
