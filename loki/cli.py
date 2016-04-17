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
        print(len(coords))
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
                                            Version: 0.1.0
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
                            type=str, default="-125.06,24.57,-67.3,49.03",
                            help=textwrap.dedent('''\
                                 Bounding box of lats/lons.
                                 Specify comma seperated list of coordinates of four
                                 coordinate points representing the four
                                 corners of the bounding box as a string. Only used if
                                 filter-type is location.'''))
        parser.add_argument('--keywords', dest='keywords', required=False,
                            type=str,
                            help=textwrap.dedent('''\
                                 Keywords to filter by.
                                 Only used if filter_type
                                 is keyword.'''))
        parser.add_argument('--location-only', dest='location_only', required=False,
                            action='store_true', default=False,
                            help=textwrap.dedent('''\
                                 If this parameter is passed, then Loki will only account
                                 for events with location attached.'''))
        parser.add_argument('--redis', dest='redis', required=False,
                            type=bool, choices=(True, False), default=False,
                            help=textwrap.dedent('''\
                                 Whether to use redis or not to
                                 push statuses to a channel.'''))
        parser.add_argument('--redis-channel', dest='redis_channel', required=False,
                            type=str, default='loki01',
                            help=textwrap.dedent('''\
                                 If the redis option is enabled, then this is the
                                 name of the channel to push statuses to.'''))
        parser.add_argument('--statistics', dest='statistics', required=False,
                            action='store_true', default=False,
                            help=textwrap.dedent('''\
                                 Collect and log statistics about what is
                                 being streamed.'''))
        parser.add_argument('--sql-db-path', dest='sql_db_path', required=False,
                            type=str,  default='/tmp/loki.db',
                            help=textwrap.dedent('''\
                                 Path to SQLite3 database to collect statistics
                                 and other data in.'''))
        parser.add_argument('--log', required=False, action='store_true',
                            dest='log', default=True,
                            help=textwrap.dedent('''\
                                Whether to enable logging.'''))
        parser.add_argument('--quiet', required=False, action='store_false',
                            dest='log', default=False,
                            help=textwrap.dedent('''\
                                Whether to silence logging.'''))
        parser.add_argument('--logfile', required=False,
                            dest='logfile', default='/tmp/lokilog.out', type=str,
                            help=textwrap.dedent('''\
                                If logging is enabled, log to
                                this filename.'''))
        return parser
