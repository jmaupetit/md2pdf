"""md2pdf tests for the core module."""

import pytest

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


def test_raises_a_validation_error_when_generated_html_is_empty():
    """Raise a ValidationError when generated HTML is empty."""
    with pytest.raises(ValidationError):
        md2pdf(OUTPUT_PDF)
