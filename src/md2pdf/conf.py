"""Configuration for md2pdf."""

MARKDOWN_BASE_EXTENSIONS: list = [
    "markdown.extensions.tables",
    "pymdownx.magiclink",
    "pymdownx.betterem",
    "pymdownx.superfences",
]

# FIXME: shouldn't be required for Linux
CLI_WATCH_FORCE_POOLING = True
