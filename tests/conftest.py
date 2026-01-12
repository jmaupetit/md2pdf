"""Tests configuration."""

import pytest

from .defaults import OUTPUT_PDF


@pytest.fixture(scope="function", autouse=True)
def remove_generated_pdf():
    """Remove test-generated PDF file."""
    yield

    # Teardown
    if OUTPUT_PDF.exists():
        OUTPUT_PDF.unlink()
