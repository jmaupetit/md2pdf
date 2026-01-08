![md2pdf logo](https://github.com/jmaupetit/md2pdf/raw/main/assets/md2pdf-logo.png)

Convert Markdown files to PDF with styles.

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jmaupetit/md2pdf/docker-image.yml?logo=docker&label=Docker%20build)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jmaupetit/md2pdf/python-package.yml?logo=python&label=Python%20build)


## Installation

The easiest way to test `md2pdf` is to use `uv`:

```bash
$ uv tool install md2pdf
```

_Nota bene:_ ensure, Weasyprint is fully functional before using md2pdf. You
will find installation instructions in the project documentation:
[https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)

## Usage

### As a CLI

```
Usage: md2pdf [OPTIONS] MD PDF

  md2pdf command line tool.

Options:
  --css PATH
  -e, --extras TEXT
  --version          Show the version and exit.
  --help             Show this message and exit.
```

For example, try to generate the project documentation with:

```bash
$ md2pdf README.md README.pdf
```

Optionally, you may load an external style:

```bash
$ md2pdf --css tests/assets/input.css README.md README.pdf
```

And/or activate [markdown
extras](https://github.com/trentm/python-markdown2/wiki/Extras):

```bash
$ md2pdf --css pygments.css -e fenced-code-blocks README.md README.pdf
```


### As a library

If you have added `md2pdf` as a dependency for your python project, you can use
`md2pdf` in your code, like:

```python
from md2pdf.core import md2pdf

md2pdf(pdf,
       md=None,
       raw=None,
       css=None,
       base_url=None,
       extras=[],
)
```

Function arguments:

* `pdf`: output PDF file path
* `raw`: input markdown raw string content
* `md`: input markdown file path
* `css`: input styles path (CSS)
* `base_url`: absolute base path for markdown linked content (as images)
* `extras`: [markdown
  extras](https://github.com/trentm/python-markdown2/wiki/Extras) that should
  be activated

### With Docker

Install [Docker](https://www.docker.com/)

Pull the image:

```bash
$ docker pull jmaupetit/md2pdf
```

Now run your image:

```bash
$ docker run --rm \
    -v $PWD:/app \
    -u "$(id -u):$(id -g)" \
    jmaupetit/md2pdf --css styles.css INPUT.MD OUTPUT.PDF
```

## Contributing

### Hacking

Clone this project first:

```bash
$ git clone git@github.com:jmaupetit/md2pdf.git
```

Install md2pdf along with its dependencies (using
[uv](https://docs.astral.sh/uv/)):

```bash
$ cd md2pdf
$ make bootstrap
```

### Running the test suite

To run the test suite:

```bash
$ make test
```

Lint the code via:

```bash
$ make lint
```

### Ease your life

If you are familiar with GNU Make, we also automate daily tasks using this
lovely tool:

```bash
$ make help
```

## License

`md2pdf` is released under the MIT License. See the bundled LICENSE file for
details.
