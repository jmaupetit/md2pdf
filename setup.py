#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
md2pdf - setup file
"""

from pathlib import Path

from setuptools import setup, find_packages


def parse_requirements(requirements, ignore=("setuptools",)):
    """
    Read dependencies from requirements file (with version numbers if any)

    Notes:
        - this implementation does not support requirements files with extra
          requirements
        - this implementation has been taken from TailorDev/Watson's setup file
    """
    with open(requirements) as f:
        packages = set()
        for line in f:
            line = line.strip()
            if line.startswith(("#", "-r", "--")):
                continue
            if "#egg=" in line:
                line = line.split("#egg=")[1]
            pkg = line.strip()
            if pkg not in ignore:
                packages.add(pkg)
        return list(packages)


about = {}
with Path("md2pdf", "version.py").open(mode="r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="md2pdf",
    version=about["__version__"],
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=parse_requirements("requirements-dev.txt"),
    author="Julien Maupetit",
    author_email="julien@maupetit.net",
    description="md2pdf, a Markdown to PDF conversion tool",
    license="MIT",
    keywords="markdown converter css pdf",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Customer Service",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
)
