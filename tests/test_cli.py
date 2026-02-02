"""md2pdf tests for the CLI."""

import json
from importlib import metadata
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Thread
from time import sleep
from unittest import mock

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


def test_generate_pdf_from_multiple_markdown_source_files(cli_runner):
    """Generate PDFs from markdown files with no output argument."""
    assert not DEFAULT_OUTPUT_PDF.exists()

    # Extra markdown file
    #
    # Should be manually deleted for python < 3.12 compatibility
    with NamedTemporaryFile(suffix=".md", delete=False) as second_md:
        second_md.write(b"# title")
        second_md.close()

        second_pdf = Path(second_md.name).with_suffix(".pdf")
        assert not second_pdf.exists()

        result = cli_runner.invoke(cli, ["-i", str(INPUT_MD), "-i", second_md.name])
        assert result.exit_code == 0

        assert DEFAULT_OUTPUT_PDF.exists()
        assert second_pdf.exists()

        # Manual cleanup
        Path(second_md.name).unlink()

    # Clean generated PDF and temporary file
    second_pdf.unlink()


def test_generate_pdf_fail_from_multiple_markdown_source_files(cli_runner):
    """Generate PDFs from markdown files with a single failure."""
    assert not DEFAULT_OUTPUT_PDF.exists()

    # Extra markdown file
    #
    # Should be manually deleted for python < 3.12 compatibility
    with (
        NamedTemporaryFile(suffix=".md", delete=False) as second_md,
        mock.patch(
            "md2pdf.cli._run_with_progress", side_effect=ValidationError
        ) as mocked_md2pdf,
    ):
        second_md.write(b"# title")
        second_md.close()

        second_pdf = Path(second_md.name).with_suffix(".pdf")
        assert not second_pdf.exists()

        result = cli_runner.invoke(cli, ["-i", str(INPUT_MD), "-i", second_md.name])
        assert result.exit_code == 1

        assert not DEFAULT_OUTPUT_PDF.exists()
        assert not second_pdf.exists()

        # Manual cleanup
        Path(second_md.name).unlink()
        assert mocked_md2pdf.call_count == 2


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


def test_generate_pdf_with_watch(cli_runner):
    """Generate a PDF from a markdown file with the watch option activated."""
    assert not OUTPUT_PDF.exists()

    # Raise a KeyboardInterrupt after the first watcher changes event
    with mock.patch("md2pdf.cli.watcher_callback", side_effect=KeyboardInterrupt):
        bg_runner = Thread(
            target=cli_runner.invoke,
            daemon=True,
            args=(
                cli,
                ["-i", str(INPUT_MD), "-o", str(OUTPUT_PDF), "-w"],
            ),
        )
        bg_runner.start()

        # Wait for the first PDF generation
        while not OUTPUT_PDF.exists():
            sleep(0.1)
        output_pdf_last_modification = OUTPUT_PDF.stat().st_mtime
        OUTPUT_PDF.unlink()
        assert not OUTPUT_PDF.exists()

        # Changing the input markdown file should raise a changes event. Wait a bit
        # before triggering the change.
        sleep(1)
        INPUT_MD.touch()

        # Wait for it
        bg_runner.join(timeout=60)

    # The PDF file should have been updated
    assert OUTPUT_PDF.exists()
    assert output_pdf_last_modification != OUTPUT_PDF.stat().st_mtime


def test_generate_pdf_with_watch_and_css(cli_runner):
    """Generate a PDF from markdown files with the watch and css options activated."""
    assert not OUTPUT_PDF.exists()

    # Raise a KeyboardInterrupt after the first watcher changes event
    #
    # The second markdown temporary file should be manually deleted for
    # python < 3.12 compatibility
    with (
        mock.patch("md2pdf.cli.watcher_callback", side_effect=KeyboardInterrupt),
        NamedTemporaryFile(suffix=".md", delete=False) as second_md,
    ):
        # Add markdown content
        second_md.write(b"# title")
        second_md.close()

        second_pdf = Path(second_md.name).with_suffix(".pdf")
        assert not second_pdf.exists()

        bg_runner = Thread(
            target=cli_runner.invoke,
            daemon=True,
            args=(
                cli,
                [
                    "-i",
                    str(INPUT_MD),
                    "-i",
                    second_md.name,
                    "-c",
                    str(INPUT_CSS),
                    "-w",
                ],
            ),
        )
        bg_runner.start()

        # Wait for all PDFs generation
        while not all((DEFAULT_OUTPUT_PDF.exists(), second_pdf.exists())):
            sleep(0.1)

        output_pdf_last_modification = DEFAULT_OUTPUT_PDF.stat().st_mtime
        second_pdf_last_modification = second_pdf.stat().st_mtime

        # Delete PDFs generated before starting the watcher
        DEFAULT_OUTPUT_PDF.unlink()
        second_pdf.unlink()
        assert not DEFAULT_OUTPUT_PDF.exists()
        assert not second_pdf.exists()

        # Changing the input CSS file should raise a changes event and both markdown
        # files should be rendered. Wait a bit for the watcher to start before
        # performing changes.
        sleep(1)
        INPUT_CSS.touch()

        # Wait for it
        bg_runner.join(timeout=60)

        # Manual cleanup
        Path(second_md.name).unlink()

    # The PDF file should have been updated
    assert DEFAULT_OUTPUT_PDF.exists()
    assert second_pdf.exists()
    assert output_pdf_last_modification != DEFAULT_OUTPUT_PDF.stat().st_mtime
    assert second_pdf_last_modification != second_pdf.stat().st_mtime
    second_pdf.unlink()
