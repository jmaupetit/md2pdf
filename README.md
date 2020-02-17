![md2pdf logo](https://github.com/jmaupetit/md2pdf/raw/master/assets/md2pdf-logo.png)

Convert Markdown files to PDF with styles.

[![Build Status](https://travis-ci.org/jmaupetit/md2pdf.svg?branch=master)](https://travis-ci.org/jmaupetit/md2pdf)
[![Coverage Status](https://coveralls.io/repos/github/jmaupetit/md2pdf/badge.svg?branch=master)](https://coveralls.io/github/jmaupetit/md2pdf?branch=master)


## Installation

The easiest way to go is to use pip:

```bash
$ pip install md2pdf
```

## Usage

### As a CLI

```
Usage:
    md2pdf [options] INPUT.MD OUTPUT.PDF

Options:
    --css=STYLE.CSS
```

For example, try to generate the project documentation with:

```bash
$ md2pdf README.md README.pdf
```

Optionally, you may load an external style (restricted to CSS2):

```bash
$ md2pdf --css tests/resources/input.css README.md README.pdf
```

### As a library

You can use `md2pdf` in your python code, like:

```python
from md2pdf.core import md2pdf

md2pdf(pdf_file_path,
       md_content=None,
       md_file_path=None,
       css_file_path=None,
       base_url=None)
```

Function arguments:

* `pdf_file_path`: output PDF file path
* `md_content`: input markdown raw string content
* `md_file_path`: input markdown file path
* `css_file_path`: input styles path (CSS)
* `base_url`: absolute base path for markdown linked content (as images)

### With Docker

Install [Docker](https://www.docker.com/)

Pull the image:

```bash
$ docker pull jmaupetit/md2pdf
```

Now run your image:

```bash
$ docker run --rm -v $PWD:/app jmaupetit/md2pdf --css styles.css INPUT.MD OUTPUT.PDF
```

## Troubleshooting on MacOSX

Ensure, Weasyprint is fully functional before using md2pdf. You will find
installation instructions in the project documentation:
[https://weasyprint.readthedocs.io/en/latest/install.html](https://weasyprint.readthedocs.io/en/latest/install.html#macos)

In a few words, here are the few steps you will need to follow:

* Install XQuartz from:
  [https://xquartz.macosforge.org](https://xquartz.macosforge.org)
* Install all dependencies at once with
  [homebrew](http://mxcl.github.io/homebrew/) and go grab a coffee (this may
  take a while):

```bash
$ brew install cairo pango gdk-pixbuf libxml2 libxslt libffi
```

## Misc

### Using custom fonts in styles

WeasyPrint does not support the `@font-face` property yet (see [project issue
28](https://github.com/Kozea/WeasyPrint/issues/28)). If you use want to use
custom fonts, you should use system fonts and define them with the `font-family`
CSS property, like:

```
font-family: 'Neutraface Condensed';
```

Note that you should only define **one single** custom font, not a substitution
list.

## Contributing

### Hacking

Clone this project first:

```bash
$ git clone git@github.com:jmaupetit/md2pdf.git
```

Install it with its dependencies (ideally in a virtual environment):

```bash
$ cd md2pdf
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements-dev.txt
(venv) $ python setup.py develop
```

### Running the test suite

To run the test suite with your active python version (virtual environment):

```bash
(venv) $ pytest
```

Lint the code via:

```bash
(venv) $ flake8
```

### Release a new version

Upload a new release to PyPI:

```
$ python setup.py sdist bdist_wheel
$ twine upload dist/* --username 'johndoe' --password 'secret'
```

## License

`md2pdf` is released under the MIT License. See the bundled LICENSE file for
details.
