# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import remove
from os.path import exists
from subprocess import PIPE, Popen

from .defaults import INPUT_CSS, INPUT_MD, OUTPUT_PDF


def setup_function(function):
    """Remove temporary PDF files"""

    if exists(OUTPUT_PDF):
        remove(OUTPUT_PDF)


def _run(cmd):
    """Run cmd in a shell"""

    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
        close_fds=True
    )
    return p.communicate()


def test_print_usage_when_no_args():

    stdout, stderr = _run('md2pdf')
    expected = 'Usage: md2pdf [options] INPUT.MD OUTPUT.PDF'
    assert expected in stderr


def test_print_usage_when_partial_args():

    stdout, stderr = _run('md2pdf input.md')
    expected = 'Usage: md2pdf [options] INPUT.MD OUTPUT.PDF'
    assert expected in stderr


def test_raise_IOError_when_markdown_input_file_does_not_exists():

    cmd = 'md2pdf input.md output.pdf'
    stdout, stderr = _run(cmd)

    expected = '[Errno 2] No such file or directory: \'input.md\''
    assert expected in stderr


def test_raise_IOError_when_stylesheet_does_not_exists():

    cmd = 'md2pdf --css=styles.css {} {}'.format(INPUT_MD, OUTPUT_PDF)
    stdout, stderr = _run(cmd)

    expected = '[Errno 2] No such file or directory: \'styles.css\''
    assert expected in stderr


def test_generate_pdf_from_markdown_source_file():

    assert not exists(OUTPUT_PDF)

    cmd = 'md2pdf {} {}'.format(INPUT_MD, OUTPUT_PDF)
    stdout, stderr = _run(cmd)
    assert exists(OUTPUT_PDF)


def test_generate_pdf_from_markdown_source_file_and_stylesheet():

    assert not exists(OUTPUT_PDF)

    cmd = 'md2pdf --css {} {} {}'.format(INPUT_CSS, INPUT_MD, OUTPUT_PDF)
    stdout, stderr = _run(cmd)
    assert exists(OUTPUT_PDF)
