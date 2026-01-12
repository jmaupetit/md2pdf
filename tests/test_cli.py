"""md2pdf tests for the CLI."""

import json

import pytest
from click.testing import CliRunner

from md2pdf.cli import cli, parse_config
from md2pdf.exceptions import ValidationError

from .defaults import INPUT_CSS, INPUT_MD, OUTPUT_PDF


@pytest.mark.parametrize(
    "config",
    (
        '{"my_extension": {"option_1": 1, "option_2": true}}',  # standard
        '{"my_extension":{"option_1":1,"option_2":true}}',  # compressed
        """
        {
          "my_extension": {
            "option_1": 1,
            "option_2": true
          }
        }
        """,  # formatted
    ),
)
def test_parse_config(config):
    """Test the input configuration parsing."""
    expected = {"my_extension": {"option_1": 1, "option_2": True}}
    assert parse_config(config) == expected


@pytest.mark.parametrize(
    "config",
    (
        "my_extension=value",  # simple string
        "{'my_extension': {'option_1': 1, 'option_2': true}}",  # single-quotes
        '{"my_extension": {"option_1": toto, "option_2": true}}',  # string w/o quotes
        '{"my_extension": {"option_1": 1, "option_2": true,}}',  # last row comma
    ),
)
def test_parse_config_invalid_config(config):
    """Test the input configuration parsing when an invalid configuration is parsed."""
    with pytest.raises(
        ValidationError,
        match=r"Invalid input configuration string \(should be valid JSON\)",
    ):
        parse_config(config)


def test_print_usage_when_no_args():
    """Print usage when no arguments are passed."""
    runner = CliRunner()
    result = runner.invoke(cli)
    expected = "Usage: md2pdf [OPTIONS] MD PDF"
    assert result.exit_code == 2
    assert expected in result.output


def test_print_usage_when_partial_args():
    """Print usage when required arguments are missing."""
    runner = CliRunner()
    result = runner.invoke(cli, ["input.md"])
    expected = "Usage: md2pdf [OPTIONS] MD PDF"
    assert result.exit_code == 2
    assert expected in result.output


def test_raise_IOError_when_markdown_input_file_does_not_exists():
    """Raise an I/O error when markdown input file does not exist."""
    runner = CliRunner()
    result = runner.invoke(cli, ["input.md", "output.pdf"])
    expected = "Error: Invalid value for 'MD': Path 'input.md' does not exist."
    assert result.exit_code == 2
    assert expected in result.output


def test_raise_IOError_when_stylesheet_does_not_exists():
    """Raise an I/O error when CSS input file does not exist."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--css=styles.css", str(INPUT_MD), str(OUTPUT_PDF)])
    expected = (
        "Error: Invalid value for '--css' / '-c': Path 'styles.css' does not exist."
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


def test_generate_pdf_with_an_extension():
    """Generate a PDF from a markdown file with an extra extension."""
    assert not OUTPUT_PDF.exists()
    runner = CliRunner()
    runner.invoke(cli, ["--extras", "footnotes", str(INPUT_MD), str(OUTPUT_PDF)])
    assert OUTPUT_PDF.exists()


def test_generate_pdf_with_a_configured_extension():
    """Generate a PDF from a markdown file with an extra configured extension."""
    assert not OUTPUT_PDF.exists()
    runner = CliRunner()
    runner.invoke(
        cli,
        [
            "--extras",
            "footnotes",
            "--config",
            json.dumps({"footnotes": {"BACKLINK_TEXT": "link"}}),
            str(INPUT_MD),
            str(OUTPUT_PDF),
        ],
    )
    assert OUTPUT_PDF.exists()
