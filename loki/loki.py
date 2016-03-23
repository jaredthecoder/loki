# -*- coding: utf-8 -*-

""" loki.py

This file contains the main routine for the entire package. Orchestrates the rest of the files.
"""


# Project assets
from loki.Harvester import Harvester
from loki.Cli import Cli
from loki.LokiLogger import LokiLogger
from loki.utils import log_if_exists


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


def start_harvester(args, logger=None):
    keywords = None
    if args.filter_type == 'keyword':
        keywords = format_keywords(args.keywords)
    log_if_exists(logger, 'Creating harvester.', 'DEBUG')
    h = Harvester(logger=logger, filter_type=args.filter_type,
                  keywords=keywords, stats=args.statistics,
                  subscribe=args.subscribe)
    log_if_exists(logger, 'Starting the stream...', 'INFO')
    h.stream()


def main():
    logger = None
    logfile_name = None

    cli = Cli()
    if cli.args.log:
        try:
            logfile_name = cli.args.logfile
        except KeyError:
            raise ValueError('Logging is enabled by the logfile name is undefined.')
        finally:
            if logfile_name is None:
                raise ValueError('Logging is enabled by the logfile name is undefined.')
        logger = LokiLogger()
        logger.setup(logfile_name)
        start_harvester(cli.args, logger)
    start_harvester(cli.args)




