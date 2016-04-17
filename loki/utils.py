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
    kw_list = []
    for kw in keywords.split(","):
        kw_list.append(kw)
    print(kw_list)
    return kw_list


def log_if_exists(logger, message, level):
    if logger is not None:
        logger.log(message, level)
