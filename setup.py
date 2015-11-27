#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "uploader",
    version = "1.0",
    package_dir = {'':'src'},
    packages = find_packages('src'),
    scripts = ['src/uploader'],
    install_requires = [
        "Flask",
        "itsdangerous",
        "Jinja2",
        "MarkupSafe",
        "uploader",
        "Werkzeug",
        "wheel"
    ]
)
