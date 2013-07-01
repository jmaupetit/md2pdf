# md2pdf

Markdown to PDF converter.

## Installation

Clone this project first and install it with its dependancies by typing:

    $ python setup.py install

### Troubleshooting on MacOSX

Ensure, Weasyprint is fully functionnal before using md2pdf. You will find installation instructions in the project documentation: [http://weasyprint.org/docs/install/#mac-os-x](http://weasyprint.org/docs/install/)

In a few words, here are the few steps you will need to follow:

* Install XQuartz from: [https://xquartz.macosforge.org](https://xquartz.macosforge.org)
* Install all dependencies at once with [homebrew](http://mxcl.github.io/homebrew/) and go grab a coffee (this may take a while):

    $ brew install cairo pango gdk-pixbuf libxml2 libxslt libffi

## Usage

Try to generate the project documentation with:

    $ md2pdf README.md README.pdf

Optionnaly, you may load an external style (restricted to CSS2):

    $ md2pdf README.md README.pdf --css markdown-css-themes/markdown2.css

For testing purpose, I defined [markdown-css-themes](https://github.com/jasonm23/markdown-css-themes) as a  git submodule. If you want to test this css resource, type:

    $ git submodule init
    $ git submodule update
