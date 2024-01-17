"""md2pdf tests for the CLI."""

from os import remove
from os.path import exists
from subprocess import run

from .defaults import INPUT_CSS, INPUT_MD, OUTPUT_PDF


def setup_function(function):
    """Remove temporary PDF files."""
    if exists(OUTPUT_PDF):
        remove(OUTPUT_PDF)


def test_print_usage_when_no_args():
    """Print usage when no arguments are passed."""
    process = run(["md2pdf"], capture_output=True, check=False)
    expected = b"Usage: md2pdf [options] INPUT.MD OUTPUT.PDF"
    assert expected in process.stderr


def test_print_usage_when_partial_args():
    """Print usage when required arguments are missing."""
    process = run(["md2pdf", "input.md"], capture_output=True, check=False)
    expected = b"Usage: md2pdf [options] INPUT.MD OUTPUT.PDF"
    assert expected in process.stderr


def test_raise_IOError_when_markdown_input_file_does_not_exists():
    """Raise an I/O error when markdown input file does not exist."""
    process = run(
        ["md2pdf", "input.md", "output.pdf"], capture_output=True, check=False
    )
    expected = b"[Errno 2] No such file or directory: 'input.md'"
    assert expected in process.stderr


def test_raise_IOError_when_stylesheet_does_not_exists():
    """Raise an I/O error when CSS input file does not exist."""
    process = run(
        ["md2pdf", "--css=styles.css", INPUT_MD, OUTPUT_PDF],
        capture_output=True,
        check=False,
    )
    expected = b"[Errno 2] No such file or directory: 'styles.css'"
    assert expected in process.stderr


def test_generate_pdf_from_markdown_source_file():
    """Generate a PDF from a markdown file."""
    assert not exists(OUTPUT_PDF)
    run(["md2pdf", INPUT_MD, OUTPUT_PDF], check=False)
    assert exists(OUTPUT_PDF)


def test_generate_pdf_from_markdown_source_file_and_stylesheet():
    """Generate a PDF from a markdown and a CSS file."""
    assert not exists(OUTPUT_PDF)
    run(["md2pdf", f"--css={INPUT_CSS}", INPUT_MD, OUTPUT_PDF], check=False)
    assert exists(OUTPUT_PDF)
