#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "uploader",
    version = "2.0.1",
    author = "Ashoka Lella",
    author_email = "ashok.lella@gmail.com",
    license = "MIT",
    packages = find_packages(),
    include_package_data=True,
    scripts = ['uploader/scripts/uploader'],
    package_data={"uploader": ['templates/*']},
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
