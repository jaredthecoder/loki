# -*- coding: utf-8 -*-

""" Cli.py

Command Line Interface for Loki
"""


# Python standard library assets
import argparse
import textwrap
from argparse import RawTextHelpFormatter


__author__ = 'Jared M Smith'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jared M Smith'
__email__ = 'jared@jaredsmith.io'


class Cli:

    def __init__(self):
        self.__parser = self.__setup_argparser()
        self.args = self.__parser.parse_args()

    def __check_location(self, coords):
        if len(coords) != 4:
            raise argparse.ArgumentTypeError(textwrap.dedent('''\
                                             Must specify only four coordinate
                                             points for the bounding box.'''))
        return list

    def __setup_argparser(self):
        parser = argparse.ArgumentParser(prog='loki',
                                         formatter_class=RawTextHelpFormatter,
                                         description=textwrap.dedent('''\
                                                    __        __    _
                                                   / /  ___  / /__ (_)
                                                  / /__/ _ \/  '_// /
                                                 /____/\___/_/\_\/_/
                                            ------------------------------------
                                            Intelligent Entity Finder
                                            Version: 0.0.1
                                            ------------------------------------
                                            '''),
                                         epilog=textwrap.dedent('''\
                                            Author: Jared M Smith
                                            Contact: jared@jaredsmith.io
                                            ''')
                                         )

        parser.add_argument('--filter-type', dest='filter_type', required=False,
                            type=str, default='location',
                            choices=('location', 'keyword'),
                            help=textwrap.dedent('''\
                                 [location/keyword] What type of filter to
                                 put on the twitter stream. Default is
                                 location.'''))
        parser.add_argument('--location', dest='location', required=False,
                            type=self.__check_location, nargs='+',
                            default=[-167.344, -57.704, 178.594, 74.9594],
                            help=textwrap.dedent('''\
                                 Bounding box of lats/lons. Specify four
                                 coordinate points representing the four
                                 corners of the bounding box. Only used if
                                 filter_type is location.'''))
        parser.add_argument('--keywords', dest='keywords', required=False,
                            type=list, nargs='+',
                            help=textwrap.dedent('''\
                                 Keywords to filter by.
                                 Only used if filter_type
                                 is keyword.'''))
        parser.add_argument('--redis', dest='redis', required=False,
                            type=bool, choices=(True, False), default=False,
                            help=textwrap.dedent('''\
                                 Whether to use redis or not to
                                 push statuses to a channel.'''))
        parser.add_argument('--redis_channel', dest='redis_channel', required=False,
                            type=str, default='loki01',
                            help=textwrap.dedent('''\
                                 If the redis option is enabled, then this is the
                                 name of the channel to push statuses to.'''))
        parser.add_argument('--statistics', dest='statistics', required=False,
                            type=bool, choices=(True, False), default=False,
                            help=textwrap.dedent('''\
                                 Collect and log statistics about what is
                                 being streamed.'''))
        parser.add_argument('--sql-db-path', dest='sql_db_path', required=False,
                            type=str,  default=False,
                            help=textwrap.dedent('''\
                                 Path to SQLite3 database to collect statistics
                                 and other data in.'''))
        parser.add_argument('--log', required=False, type=bool,
                            choices=(True, False),
                            dest='log', default=True,
                            help=textwrap.dedent('''\
                                Whether to enable logging.
                                Defaults to True. Possible options are
                                (True, False).'''))
        parser.add_argument('--logfile', required=False,
                            dest='logfile', type=str,
                            help=textwrap.dedent('''\
                                If logging is enabled, log to
                                this filename.'''))
        return parser
