# -*- coding: utf-8 -*-

""" utils.py

Various utilities
"""


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


def log_if_exists(logger, message, level):
    if logger is not None:
        logger.log(message, level)
