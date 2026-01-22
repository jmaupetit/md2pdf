"""Tests configuration."""

import pytest
from typer.testing import CliRunner

from .defaults import DEFAULT_OUTPUT_PDF, OUTPUT_PDF


@pytest.fixture(scope="function", autouse=True)
def remove_generated_pdf():
    """Remove test-generated PDF file."""
    yield

    # Teardown
    if OUTPUT_PDF.exists():
        OUTPUT_PDF.unlink()
    if DEFAULT_OUTPUT_PDF.exists():
        DEFAULT_OUTPUT_PDF.unlink()


@pytest.fixture
def cli_runner():
    """CLI runner."""
    yield CliRunner()
