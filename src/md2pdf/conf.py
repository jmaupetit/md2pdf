"""Configuration for md2pdf."""

from pathlib import Path

MARKDOWN_BASE_EXTENSIONS: list = [
    "markdown.extensions.footnotes",
    "markdown.extensions.tables",
    "markdown.extensions.toc",
    "pymdownx.betterem",
    "pymdownx.caret",
    "pymdownx.emoji",
    "pymdownx.magiclink",
    "pymdownx.magiclink",
    "pymdownx.mark",
    "pymdownx.superfences",
    "pymdownx.tilde",
]

# FIXME: shouldn't be required for Linux
CLI_WATCH_FORCE_POOLING = True

# Templates
BASE_TEMPLATE = Path(__file__).parent / Path("./templates/base.html.j2")
