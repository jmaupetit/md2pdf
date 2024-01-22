"""md2pdf tests for the CLI."""

from os import remove
from os.path import exists
from subprocess import run

from click.testing import CliRunner

from md2pdf.cli import cli
from .defaults import INPUT_CSS, INPUT_MD, OUTPUT_PDF


def setup_function(function):
    """Remove temporary PDF files."""
    if exists(OUTPUT_PDF):
        remove(OUTPUT_PDF)


def test_print_usage_when_no_args():
    """Print usage when no arguments are passed."""
    runner = CliRunner()
    result = runner.invoke(cli)
    expected = "Usage: md2pdf [OPTIONS] MD_FILE_PATH PDF_FILE_PATH"
    assert result.exit_code == 2
    assert expected in result.output


def test_print_usage_when_partial_args():
    """Print usage when required arguments are missing."""
    runner = CliRunner()
    result = runner.invoke(cli, ["input.md"])
    expected = "Usage: md2pdf [OPTIONS] MD_FILE_PATH PDF_FILE_PATH"
    assert result.exit_code == 2
    assert expected in result.output


def test_raise_IOError_when_markdown_input_file_does_not_exists():
    """Raise an I/O error when markdown input file does not exist."""
    runner = CliRunner()
    result = runner.invoke(cli, ["input.md", "output.pdf"])
    expected = (
        "Error: Invalid value for 'MD_FILE_PATH': Path 'input.md' does not exist."
    )
    assert result.exit_code == 2
    assert expected in result.output


def test_raise_IOError_when_stylesheet_does_not_exists():
    """Raise an I/O error when CSS input file does not exist."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--css=styles.css", str(INPUT_MD), str(OUTPUT_PDF)])
    expected = (
        "Error: Invalid value for '--css': Path 'styles.css' does not exist."
    )
    assert result.exit_code == 2
    assert expected in result.output


def test_generate_pdf_from_markdown_source_file():
    """Generate a PDF from a markdown file."""
    assert not OUTPUT_PDF.exists()
    runner = CliRunner()
    runner.invoke(cli, [str(INPUT_MD), str(OUTPUT_PDF)])
    assert OUTPUT_PDF.exists()


def test_generate_pdf_from_markdown_source_file_and_stylesheet():
    """Generate a PDF from a markdown and a CSS file."""
    assert not OUTPUT_PDF.exists()
    runner = CliRunner()
    runner.invoke(cli, [f"--css={INPUT_CSS}", str(INPUT_MD), str(OUTPUT_PDF)])
    assert OUTPUT_PDF.exists()
