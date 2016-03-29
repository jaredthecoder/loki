# -*- coding: utf-8 -*-


import re
from distutils.core import setup


with open('README.md', 'rb') as f:
    long_descr = f.read().decode('utf-8')


setup(
    name = 'loki',
    packages = ['loki'],
    entry_points = {
        'console_scripts': ['loki = loki.loki.main']
        },
    version = '0.1.0',
    description = 'Intelligent Entity Finder',
    long_description = long_descr,
    author = 'Jared M Smith',
    author_email = 'jared@jaredsmith.io',
    install_requires=[
    ],
)
