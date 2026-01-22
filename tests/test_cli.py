"""md2pdf tests for the CLI."""

import json
from importlib import metadata

import pytest

from md2pdf.cli import cli, parse_config
from md2pdf.exceptions import ValidationError

from .defaults import DEFAULT_OUTPUT_PDF, INPUT_CSS, INPUT_MD, OUTPUT_PDF


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


def test_print_usage_when_no_args(cli_runner):
    """Print usage when no arguments are passed."""
    result = cli_runner.invoke(cli)
    expected = "Usage: main [OPTIONS]"
    assert result.exit_code == 2
    assert expected in result.output


def test_exit_when_no_markdown_input(cli_runner):
    """Exit with an error message when not input markdown files are passed."""
    result = cli_runner.invoke(cli, ["-o", "test.pdf"])
    expected = "No markdown input file. See `--help`"
    assert result.exit_code == 2
    assert expected in result.output


def test_exit_when_multiple_markdown_and_pdf_options(cli_runner):
    """Exit with an error message when called with multitple input & output options."""
    result = cli_runner.invoke(
        cli, ["-i", str(INPUT_MD), "-i", str(INPUT_MD), "-o", "test.pdf"]
    )
    expected = "PDF output option `--output/-o` cannot be used with multiple input."
    assert result.exit_code == 2
    assert expected in result.output


def test_command_version(cli_runner):
    """Print program version when asked."""
    result = cli_runner.invoke(cli, "-V")
    expected = metadata.version("md2pdf")
    assert result.exit_code == 0
    assert expected in result.output


def test_command_raise_error_when_markdown_input_file_does_not_exists(cli_runner):
    """Raise an I/O error when markdown input file does not exist."""
    result = cli_runner.invoke(cli, ["-i", "input.md"])
    expected = "Invalid value for '--input' / '-i': Path 'input.md' does not exist."
    assert result.exit_code == 2
    assert expected in result.output


def test_command_raise_error_when_stylesheet_does_not_exists(cli_runner):
    """Raise an I/O error when CSS input file does not exist."""
    result = cli_runner.invoke(
        cli, ["-c", "styles.css", "-i", str(INPUT_MD), "-o", str(OUTPUT_PDF)]
    )
    expected = "Invalid value for '--css' / '-c': Path 'styles.css' does not exist."
    assert result.exit_code == 2
    assert expected in result.output


def test_generate_pdf_from_markdown_source_file(cli_runner):
    """Generate a PDF from a markdown file."""
    assert not OUTPUT_PDF.exists()
    result = cli_runner.invoke(cli, ["-i", str(INPUT_MD), "-o", str(OUTPUT_PDF)])
    assert result.exit_code == 0
    assert OUTPUT_PDF.exists()


def test_generate_pdf_from_markdown_source_file_without_output(cli_runner):
    """Generate a PDF from a markdown file with no output argument."""
    assert not DEFAULT_OUTPUT_PDF.exists()
    result = cli_runner.invoke(cli, ["-i", str(INPUT_MD)])
    assert result.exit_code == 0
    assert DEFAULT_OUTPUT_PDF.exists()


def test_generate_pdf_from_markdown_source_file_and_stylesheet(cli_runner):
    """Generate a PDF from a markdown and a CSS file."""
    assert not OUTPUT_PDF.exists()
    result = cli_runner.invoke(
        cli, ["-c", str(INPUT_CSS), "-i", str(INPUT_MD), "-o", str(OUTPUT_PDF)]
    )
    assert result.exit_code == 0
    assert OUTPUT_PDF.exists()


def test_generate_pdf_with_an_extension(cli_runner):
    """Generate a PDF from a markdown file with an extra extension."""
    assert not OUTPUT_PDF.exists()
    cli_runner.invoke(
        cli, ["--extras", "footnotes", "-i", str(INPUT_MD), "-o", str(OUTPUT_PDF)]
    )
    assert OUTPUT_PDF.exists()


def test_generate_pdf_with_a_configured_extension(cli_runner):
    """Generate a PDF from a markdown file with an extra configured extension."""
    assert not OUTPUT_PDF.exists()
    cli_runner.invoke(
        cli,
        [
            "-e",
            "footnotes",
            "-C",
            json.dumps({"footnotes": {"BACKLINK_TEXT": "link"}}),
            "-i",
            str(INPUT_MD),
            "-o",
            str(OUTPUT_PDF),
        ],
    )
    assert OUTPUT_PDF.exists()
