---
title: Welcome
icon: lucide/rocket
---

<center>
  <img src="./images/md2pdf-logo.png" alt="md2pdf logo" title="Convert Markdown to PDF with styles!" />
</center>

## The idea 💡

**TL;DR** `md2pdf` is a python library **and** a command line interface (_aka_
CLI) that converts plain
[Markdown](https://daringfireball.net/projects/markdown/) sources to rendered
PDF files. It's key features are:

1. 💅 **styles**: you can provide a custom Stylesheet (CSS) to make your documents look shiny.
2. 🚸 **templates**: every Markdown content can leverage the power of the [Jinja](https://jinja.palletsprojects.com/en/stable/) templating engine.


=== "Markdown"

    ```` md title="idea.md"
    --8<-- "docs/snippets/idea.md"
    `````

=== "PDF"

    <iframe
      type="application/pdf"
      src="./snippets/idea.pdf"
      width="100%"
      height="500"
      title="Idea PDF">
    </iframe>


## Quick start guide

`md2pdf` can be used either as a python library or
