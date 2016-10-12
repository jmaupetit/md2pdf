![md2pdf logo](./assets/md2pdf-logo.png)

Convert Markdown files to PDF with styles.

## Installation

Clone this project first and install it with its dependencies (ideally in a
virtualenv, see the [virtualenvwrapper project
documentation](http://virtualenvwrapper.readthedocs.org/en/latest/index.html))
by typing:

```bash
$ python setup.py install
```

### Troubleshooting on MacOSX

Ensure, Weasyprint is fully functionnal before using md2pdf. You will find
installation instructions in the project documentation:
[http://weasyprint.org/docs/install/](http://weasyprint.org/docs/install/#mac-os-x)

In a few words, here are the few steps you will need to follow:

* Install XQuartz from:
  [https://xquartz.macosforge.org](https://xquartz.macosforge.org)
* Install all dependencies at once with
  [homebrew](http://mxcl.github.io/homebrew/) and go grab a coffee (this may
  take a while):

```bash
$ brew install cairo pango gdk-pixbuf libxml2 libxslt libffi
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

Optionnaly, you may load an external style (restricted to CSS2):

```bash
$ md2pdf README.md README.pdf --css markdown-css-themes/markdown2.css
```

For testing purpose, I defined
[markdown-css-themes](https://github.com/jasonm23/markdown-css-themes) as a  git
submodule. If you want to test this css resource, type:

```bash
$ git submodule init
$ git submodule update
```

### As a library

You can use md2pdf in your python code, like:

```python
from md2pdf.core import md2pdf

md2pdf(pdf_file_path,
       md_content=None,
       md_file_path=None,
       css_file_path=None,
       base_url=None)
```

See the
[md2pdf](https://github.com/jmaupetit/md2pdf/blob/master/md2pdf/core.py#L15)
function's documentation for details.

### With Docker

Install [Docker](https://www.docker.com/)

Pull the image

```bash
$ docker pull jmaupetit/md2pdf
```

Now run your image:

```bash
$ docker run --rm -v $PWD:/srv jmaupetit/md2pdf --css styles.css INPUT.MD OUTPUT.PDF
```

## Misc

### Using custom fonts in styles

WeasyPrint does not support the `@font-face` property yet (see [project issue
28](https://github.com/Kozea/WeasyPrint/issues/28)). If you use want to use
custom fonts, you should use system fonts and define them with the `font-family`
CSS property, like:

```css
font-family: 'Neutraface Condensed';
```

Note that you should only define **one single** custom font, not a substitution
list.
