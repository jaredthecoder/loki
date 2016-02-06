# -*- coding: utf-8 -*-

""" loki.py

This file contains the main routine for the entire package. Orchestrates the rest of the files.
"""


# Project assets
from loki.Harvester import Harvester
from loki.Cli import Cli


__author__ = 'Jared M Smith'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jared M Smith'
__email__ = 'jared@jaredsmith.io'


def format_keywords(keywords):
    fmt_keywords = []
    for term_breakdown in keywords:
        kwd = "".join(term_breakdown)
        fmt_keywords.append(kwd)
    return ",".join(fmt_keywords)


def start_harvester(args):
    keywords = None
    if args.filter_type == 'keyword':
        keywords = format_keywords(args.keywords)
    h = Harvester(filter_type=args.filter_type, keywords=keywords)
    h.stream()


def main():
    cli = Cli()
    start_harvester(cli.args)




