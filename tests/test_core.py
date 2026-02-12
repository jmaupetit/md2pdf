"""md2pdf tests for the core module."""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
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
    md2pdf(OUTPUT_PDF, raw=raw)
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
    md2pdf(OUTPUT_PDF, raw=raw, context={"name": "John", "id": 2})
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
    md2pdf(OUTPUT_PDF, raw=raw, context={"name": "John"})
    assert OUTPUT_PDF.exists()

    # Content
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "Hey Jane 👋\nID: 2"


def test_raises_a_validation_error_when_generated_html_is_empty():
    """Raise a ValidationError when generated HTML is empty."""
    with pytest.raises(ValidationError):
        md2pdf(OUTPUT_PDF)


def test_generate_pdf_using_default_template():
    """Generate a PDF using the default template."""
    assert not OUTPUT_PDF.exists()

    # Default PDF title
    md2pdf(OUTPUT_PDF, raw="# hi there!")
    assert OUTPUT_PDF.exists()
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "hi there!"
    assert reader.metadata.title == "Generated with md2pdf"

    # Custom PDF title as a context dict
    md2pdf(
        OUTPUT_PDF, raw="# hi there!", context={"pdf": {"title": "Welcome to md2pdf"}}
    )
    assert OUTPUT_PDF.exists()
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "hi there!"
    assert reader.metadata.title == "Welcome to md2pdf"

    # Custom title in frontmatter
    md2pdf(
        OUTPUT_PDF,
        raw="\n".join(
            [
                "---",
                "pdf:",
                "  title: Welcome (again) to md2pdf",
                "---",
                "# hi there!",
            ]
        ),
    )
    assert OUTPUT_PDF.exists()
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "hi there!"
    assert reader.metadata.title == "Welcome (again) to md2pdf"


def test_generate_pdf_context_cannot_override_content_variable():
    """Assert the content context variable cannot be override."""
    assert not OUTPUT_PDF.exists()

    # Try to override default template content
    md2pdf(OUTPUT_PDF, raw="# hi there!", context={"content": "I will not be accepted"})
    assert OUTPUT_PDF.exists()
    reader = PdfReader(OUTPUT_PDF)
    assert reader.pages[0].extract_text() == "hi there!"


def test_generate_pdf_using_custom_template():
    """Generate a PDF using a custom template."""
    assert not OUTPUT_PDF.exists()

    # Should be manually deleted for python < 3.12 compatibility
    with NamedTemporaryFile(delete=False) as custom_template:
        custom_template.write(
            b"""
            <html lang="en">
              <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>{{ pdf.title }}</title>
              </head>
              <body>
                <h1>{{ title }}</h1>
                {{ content }}
                By {{ signature }}
              </body>
            </html>
            """
        )
        custom_template.close()
        custom_template_path = Path(custom_template.name)
        md2pdf(
            OUTPUT_PDF,
            raw="Come gather 'round people",
            context={
                "title": "The Times They Are a-Changin'",
                "signature": "Robert Zimmerman",
                "pdf": {"title": "Bob dylan lyrics"},
            },
            template=custom_template_path,
        )
    # Manual cleanup
    custom_template_path.unlink()

    assert OUTPUT_PDF.exists()
    reader = PdfReader(OUTPUT_PDF)
    content = reader.pages[0].extract_text()
    assert "The Times They Are a-Changin'" in content
    assert "Come gather 'round people" in content
    assert "By Robert Zimmerman" in content
    assert reader.metadata.title == "Bob dylan lyrics"
