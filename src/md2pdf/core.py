"""md2pdf core module."""

import logging
from pathlib import Path
from typing import List, Optional

import frontmatter
from jinja2 import Template
from markdown import markdown
from weasyprint import CSS, HTML

from .conf import BASE_TEMPLATE, MARKDOWN_BASE_EXTENSIONS
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
    template: Path = BASE_TEMPLATE,
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
        template: base document template

    Returns:
        None

    Raises:
        ValidationError: if md_content and md_file_path are empty.
    """
    context = context if context else {}
    # Warning: "content" variable cannot be override
    context.pop("content", None)

    extras_config = extras_config if extras_config else {}

    # Merge base extensions with extras extensions
    extras = extras if extras and len(extras) else []

    input_md: str | None = raw
    if md:
        logger.debug("Reading markdown content from file %s", md)
        input_md = md.read_text()

    if input_md is None or not len(input_md):
        raise ValidationError(
            "No markdown content to process (empty file or raw string)"
        )

    # Check if markdown file contains a frontmatter header extract context from it
    if frontmatter.checks(input_md):
        logger.info("Markdown input file contains frontmatter header")

        # Get context and the template
        ftmt_context, input_md = frontmatter.parse(input_md)
        logger.debug("Frontmatter context %s", context)
        context.update(ftmt_context)

    # Render (markdown) jinja template
    input_md = Template(input_md).render(context)

    # Render markdown to HTML
    extensions: List[str] = MARKDOWN_BASE_EXTENSIONS + extras
    inner_html = markdown(
        input_md, extensions=extensions, extension_configs=extras_config
    )

    # Render the template
    full_context = {"content": inner_html, "pdf": {"title": "Generated with md2pdf"}}
    full_context.update(context)

    input_html = Template(template.read_text()).render(full_context)
    logger.debug("Input HTML that will be sent to Weasyprint: {input_html}")

    # Weasyprint HTML object
    if base_url is None:
        base_url = Path.cwd()
    html: HTML = HTML(string=input_html, base_url=str(base_url))

    # Get styles
    styles: list = []
    if css:
        styles.append(CSS(filename=css))

    # Generate PDF
    html.write_pdf(pdf, stylesheets=styles)
