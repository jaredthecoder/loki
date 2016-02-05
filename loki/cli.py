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
        self.parser = self.setup_argparser()
        self.args = self.parser.parse_args()

    def check_location(self, coords):
        if len(coords) != 4:
            raise argparse.ArgumentTypeError(textwrap.dedent('''\
                                             Must specify only four coordinate
                                             points for the bounding box.'''))
        return list

    def setup_argparser(self):
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

        parser.add_argument('--filter_type', dest='filter_type', required=False,
                            type=str, default='location',
                            choices=('location', 'keyword'),
                            help=textwrap.dedent('''\
                                 [location/keyword] What type of filter to
                                 put on the twitter stream. Default is
                                 location.'''))
        parser.add_argument('--location', dest='location', required=False,
                            type=self.check_location, nargs='+',
                            help=textwrap.dedent('''\
                                 Bounding box of lats/lons. Specify four
                                 coordinate points representing the four
                                 corners of the bounding box. Only used if
                                 filter_type is location.'''))
        parser.add_argument('--keywords', dest='keywords', required=False,
                            type=list, nargs='+',
                            help=textwrap.dedent('''\
                                 Keywords to filter by. Only used if filter_type
                                 is keyword.'''))
        parser.add_argument('--log', required=False, type=bool,
                            choices=(True,False),
                            dest='log', default=True,
                            help=textwrap.dedent('''\
                                Whether to enable logging.
                                Defaults to True. Possible options are
                                (True, False).'''))
        parser.add_argument('--logfile', required=False,
                            dest='log_file', type=str,
                            help=textwrap.dedent('''\
                                If logging is enabled, log to
                                this file.'''))
        return parser
