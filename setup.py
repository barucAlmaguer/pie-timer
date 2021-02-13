#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from src import __version__

requirements = [
    # TODO: put package requirements here
    'pydash==4.8.0',
    'click==7.1.2',
    'pytz==2020.1',
    'tzlocal==2.1',
    'colorama==0.4.3',
    'termcolor==1.1.0',
    'python-dateutil==2.8.1'
]

setup_requirements = [
    # TODO: put setup requirements (distutils extensions, etc.) here
    'twine'
]

test_requirements = [
    # TODO: put package test requirements here
    'pytest',
    'pytest-cov'
]

desc = "CLI timer and time management utils / reports"
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pie-timer',
    version=__version__,
    description=desc,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Baruc Almaguer",
    author_email="baruc.almaguer@gmail.com",
    url='https://github.com/barucAlmaguer/pie-timer',
    packages=find_packages(include=['src']),
    entry_points={
        'console_scripts': [
            'pie=src.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=['cli', 'timer', 'chronometer', 'time management'],
    test_suite='pytest',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
