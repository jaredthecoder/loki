# -*- coding: utf-8 -*-


import re
from distutils.core import setup


version = re.search(
    '^__version__\s*=\*"(.*)"',
    open('loki/loki.py').read(),
    re.M
    ).group(1)


with open('README.md', 'rb') as f:
    long_descr = f.read().decode('utf-8')


setup(
    name = 'loki',
    packages = ['loki'],
    entry_points = {
        'console_scripts': ['loki = loki.loki.main']
        },
    version = version,
    description = 'Intelligent Entity Finder',
    long_description = long_descr,
    author = 'Jared M Smith',
    author_email = 'jared@jaredsmith.io',
    install_requires=[
    ],
)
