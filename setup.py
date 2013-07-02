#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
md2pdf - Installation script
"""

from setuptools import setup, find_packages

VERSION = '0.2'

setup(
    name = "md2pdf",
    version = VERSION,
    packages = find_packages(),
    scripts = ['scripts/md2pdf',],
    install_requires = open('requirements.txt').readlines(),
    author = "Julien Maupetit",
    author_email = "julien@maupetit.net",
    description = "md2pdf, a Markdown to PDF conversion tool",
    license = "MIT",
)
