---
title: Welcome to md2pdf
icon: lucide/rocket
---

<center>
  <img src="./images/md2pdf-logo.png" alt="md2pdf logo" title="Convert Markdown to PDF with styles!" />
</center>

## The idea 💡

**TL;DR** `md2pdf` is a python library **and** a command line interface (_aka_
CLI) that converts plain
[Markdown](https://daringfireball.net/projects/markdown/) sources to rendered
PDF files.

## Key features ✨

1. **Styles**: you can provide a custom Stylesheet (CSS) to make your documents look shiny.
2. **Templates**: every Markdown content can leverage the power of the [Jinja](https://jinja.palletsprojects.com/en/stable/) templating engine.

=== "Markdown (input)"

    ```` md title="idea.md"
    --8<-- "docs/snippets/idea.md"
    ````

=== "PDF (output)"

    <iframe
      type="application/pdf"
      src="./snippets/idea.pdf"
      width="100%"
      height="500"
      title="Idea PDF">
    </iframe>

## Quick start guide

`md2pdf` can be used either as a python library or
