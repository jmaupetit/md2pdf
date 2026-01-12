"""md2pdf core module."""

import logging
from pathlib import Path
from typing import List, Optional

import frontmatter
from jinja2 import Template
from markdown import markdown
from weasyprint import CSS, HTML

from .conf import MARKDOWN_BASE_EXTENSIONS
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


def md2pdf(
    pdf: Path,
    raw: Optional[str] = None,
    md: Optional[Path] = None,
    css: Optional[Path] = None,
    base_url: Optional[Path] = None,
    extras: Optional[List[str]] = None,
    extras_config: Optional[dict] = None,
    context: Optional[dict] = None,
):
    """Converts input markdown to styled HTML and renders it to a PDF file.

    Args:
        pdf: output PDF file path.
        md: input markdown file path.
        raw: input markdown raw string content.
        css: input styles path (CSS).
        base_url: absolute base path for markdown linked content (as images).
        extras: supplementary markdown extensions to activate
        extras_config: a configuration dictionnary for active markdown extensions
        context: input context to use for jinja template rendering

    Returns:
        None

    Raises:
        ValidationError: if md_content and md_file_path are empty.
    """
    context = context if context else {}
    extras_config = extras_config if extras_config else {}

    # Merge base extensions with extras extensions
    extras = extras if extras and len(extras) else []

    if md:
        logger.debug("Reading markdown content from file %s", md)
        raw = md.read_text()

    if raw is None or not len(raw):
        raise ValidationError(
            "No markdown content to process (empty file or raw string)"
        )

    # Check if markdown file is a template
    if frontmatter.checks(raw):
        logger.info("Markdown input file contains frontmatter header")

        # Get context and the template
        ftmt_context, raw = frontmatter.parse(raw)
        logger.debug("Frontmatter context %s", context)
        context.update(ftmt_context)

    # Render the template
    raw = Template(raw).render(context)

    extensions = MARKDOWN_BASE_EXTENSIONS + extras
    raw_html = markdown(raw, extensions=extensions, extension_configs=extras_config)

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
