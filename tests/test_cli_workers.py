"""md2pdf tests for the CLI workers option.

WeasyPrint requires system libraries (Pango) that may be missing, so it is
stubbed here like the pure-parsing tests do; these tests never reach PDF
rendering (they exit during option validation).
"""

import sys
from unittest.mock import MagicMock

import pytest

sys.modules.setdefault("weasyprint", MagicMock())

from md2pdf.cli import cli

from .defaults import INPUT_MD


@pytest.mark.parametrize(
    "option",
    (
        ["-W", "0"],
        ["--workers", "0"],
        ["--workers=-1"],
    ),
)
def test_exit_when_workers_not_positive(cli_runner, option):
    """Exit with an error message when workers is not a positive integer."""
    result = cli_runner.invoke(cli, ["-i", str(INPUT_MD), *option])
    expected = "Option `--workers/-W` must be a positive integer."
    assert result.exit_code == 2
    assert expected in result.output
