"""Configuration for md2pdf."""

from pathlib import Path

MARKDOWN_BASE_EXTENSIONS: list = [
    "markdown.extensions.tables",
    "pymdownx.magiclink",
    "pymdownx.betterem",
    "pymdownx.superfences",
]

# FIXME: shouldn't be required for Linux
CLI_WATCH_FORCE_POOLING = True

# Templates
BASE_TEMPLATE = Path(__file__).parent / Path("./templates/base.html.j2")
