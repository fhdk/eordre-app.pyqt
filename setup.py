#!/bin/env python

import io
import os
import re

from setuptools import setup


def read(*names, **kwargs):
    """read"""
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """get version"""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to get version string.")


with open('README.md') as readme_file:
    README = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    CHANGELOG = changelog_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='eordre-app.pyqt',
    version=find_version("version.py"),
    packages=['util', 'models', 'dialogs', 'resources', 'configuration'],
    url='https://github.com/fhdk/eordre-app.pyqt',
    license='AGPL',
    author='Frede Hundewadt',
    author_email='echo "ZmhAdWV4LmRrCg==" | base64 -d',
    description='Eordre app build with Python 3 and PyQt5',
    long_description=README + '\n\n' + CHANGELOG,
    requires=['PyQt5'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End User/Desktop',
        'License :: OSI Approved :: AGPL License',
        'Natural Language :: Danish',
        'Programming Language :: Python :: 3.6',
        'Environment :: GUI',
        'Operating System :: Linux :: Linux',
        'Operating System :: Apple :: macOS',
        'Operating System :: Microsoft :: Windows',
    ]
)
