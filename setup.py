#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pytumb

setup(name="pytumb",
    version=pytumb.__vesion__,
    description="Tumblr library for Python",
    long_description=file('README.md').read(),
    license=pytumb.__license__,
    author=pytumb.__author__,
    url=pytumb.__url__,
    packages = find_packages(),
    keywords = [
        'tumblr'
    ],
    classifiers = [ # http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe = False,
    install_requires=[
        'requests>=0.13.2',
        'requests-oauth>=0.4.1',
        'pytz>=2012c',
        'simplejson>=2.6.0',
        ]
)