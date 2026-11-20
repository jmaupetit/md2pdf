"""md2pdf tests for the core module."""

import pytest
from jinja2.exceptions import SecurityError
from pypdf import PdfReader

from md2pdf import md2pdf
from md2pdf.exceptions import ValidationError

from .defaults import INPUT_MD, OUTPUT_PDF


def test_generate_pdf_from_markdown_file():
    """Generate a PDF from markdown file content."""
    assert not OUTPUT_PDF.exists()

    md2pdf(pdf=OUTPUT_PDF, md=INPUT_MD)
    assert OUTPUT_PDF.exists()


def test_generate_pdf_from_raw_markdown():
    """Generate a PDF from raw markdown content."""
    assert not OUTPUT_PDF.exists()

    md2pdf(OUTPUT_PDF, raw="# hi there!")
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "hi there!"


def test_generate_pdf_with_jinja_frontmatter_input():
    """Generate a PDF using a frontmatter header source and a Jinja template."""
    assert not OUTPUT_PDF.exists()

    raw = "\n".join(
        [
            "---",
            "name: John",
            "id: 2",
            "---",
            "Hey {{ name }} 👋\n",
            "ID: {{ id }}",
        ]
    )
    md2pdf(OUTPUT_PDF, raw=raw, render_template=True)
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "Hey John 👋\nID: 2"


def test_generate_pdf_with_jinja_context_input():
    """Generate a PDF using an input context and Jinja template."""
    assert not OUTPUT_PDF.exists()

    raw = "\n".join(
        [
            "Hey {{ name }} 👋\n",
            "ID: {{ id }}",
        ]
    )
    md2pdf(OUTPUT_PDF, raw=raw, context={"name": "John", "id": 2}, render_template=True)
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "Hey John 👋\nID: 2"


def test_generate_pdf_with_jinja_frontmatter_and_context_input():
    """Generate a PDF using a frontmatter header source, a context and a template.

    Frontmatter value takes precedence over direct context.
    """
    assert not OUTPUT_PDF.exists()

    raw = "\n".join(
        [
            "---",
            "name: Jane",
            "id: 2",
            "---",
            "Hey {{ name }} 👋\n",
            "ID: {{ id }}",
        ]
    )
    md2pdf(OUTPUT_PDF, raw=raw, context={"name": "John"}, render_template=True)
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "Hey Jane 👋\nID: 2"


def test_generate_pdf_without_template_renders_jinja_tags_literally():
    """Generate a PDF without template rendering: Jinja tags are not interpreted."""
    assert not OUTPUT_PDF.exists()

    raw = "Hey {{ name }}"
    md2pdf(OUTPUT_PDF, raw=raw, context={"name": "John"})
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "Hey {{ name }}"


def test_generate_pdf_with_template_renders_jinja_loops():
    """Generate a PDF with template rendering: Jinja loops keep working."""
    assert not OUTPUT_PDF.exists()

    raw = "\n".join(
        [
            "---",
            "groceries:",
            "  - apple",
            "  - orange",
            "---",
            "Result: {% for item in groceries %}{{ item }}, {% endfor %}",
        ]
    )
    md2pdf(OUTPUT_PDF, raw=raw, render_template=True)
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "Result: apple, orange, "


def test_generate_pdf_with_template_blocks_unsafe_attribute_access():
    """Generate a PDF with template rendering: unsafe attribute access is blocked.

    The sandbox should prevent template expressions from reaching Python
    internals (server-side template injection).
    """
    assert not OUTPUT_PDF.exists()

    raw = "{{ cycler.__init__.__globals__.os }}"
    with pytest.raises(SecurityError):
        md2pdf(OUTPUT_PDF, raw=raw, render_template=True)
    assert not OUTPUT_PDF.exists()


def test_raises_a_validation_error_when_generated_html_is_empty():
    """Raise a ValidationError when generated HTML is empty."""
    with pytest.raises(ValidationError):
        md2pdf(OUTPUT_PDF)
