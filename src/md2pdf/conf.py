"""Configuration for md2pdf."""

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
