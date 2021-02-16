# -*- coding: utf-8 -*-

# Learn more: 

from setuptools import setup, find_packages
import os
from importlib import resources
# =============================================================================>
# readme
with open('./README.md') as f:
    README = f.read()
# =============================================================================>
# license
with open('LICENSE') as f:
    LICENSE = f.read()
# =============================================================================>
# requires
print("--------------------")
with open('requirements.txt') as f:
    REQUIRES = []
    require = f.readline()
    while require:
        print(require)
        REQUIRES.append(require)
        require = f.readline()
print("--------------------")
# =============================================================================>
# package data
PACKAGE_DATA = {}
# =============================================================================>
# author
AUTHOR = 'nakashimas'
AUTHOR_EMAIL = ''
# =============================================================================>
# description
DESCRIPTION = 'python console anime'
# =============================================================================>
# version
VERSION = "0.0.0"
# =============================================================================>
setup(
    name = 'pyConsoleAnime',
    version = VERSION,
    description = DESCRIPTION,
    long_description = README,
    license = LICENSE,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = 'https://github.com/nakashimas/pyConsoleAnime',
    packages = find_packages(exclude=('tests', 'docs', 'dest', 'build')),
    package_data = PACKAGE_DATA,
    install_requires = REQUIRES,
    include_package_data = True,
    test_suite = 'tests'
)
