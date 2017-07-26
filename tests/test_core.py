# -*- coding: utf-8 -*-
import pytest

from os import remove
from os.path import exists

from md2pdf import md2pdf
from md2pdf.exceptions import ValidationError

from .defaults import OUTPUT_PDF


def setup_function(function):
    """Remove temporary PDF files"""

    if exists(OUTPUT_PDF):
        remove(OUTPUT_PDF)


def test_generate_pdf_from_raw_markdown():

    assert not exists(OUTPUT_PDF)

    md2pdf(OUTPUT_PDF, md_content='# hi there!')
    assert exists(OUTPUT_PDF)


def test_raises_a_validation_error_when_generated_html_is_empty():

    with pytest.raises(ValidationError):
        md2pdf(OUTPUT_PDF)
