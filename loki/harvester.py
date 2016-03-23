# -*- coding: utf-8 -*-

""" Harvester.py

Ingests the Twitter Streaming API
"""


# Python standard library assets
import sys

# 3rd Party assets
import tweepy

# Project assets
from loki.settings import Settings
from loki.LokiStreamListener import LokiStreamListener
from loki.utils import log_if_exists


__author__ = 'Jared M Smith'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jared M Smith'
__email__ = 'jared@jaredsmith.io'


# Harvester class consumes the twitter feed and pushes tweets onto the queue.
class Harvester(object):

    # Bounding box on US: -125.06,24.57,-67.3,49.03]
    # Whole World Two corners:
    # SW: -57.704, -167.344
    # NE: 74.9594, 178.594
    # Initialize the class
    def __init__(self, logger=None, filter_type='location',
                 location=[-167.344, -57.704, 178.594, 74.9594],
                 keywords=None, statistics=False):
        self.logger = logger
        self.filter_type = filter_type
        self.location = location

        log_if_exists(self.logger, self.location, 'DEBUG')

        self.keywords = keywords
        self.statistics = statistics
        self.settings = Settings()
        self.auth = tweepy.OAuthHandler(self.settings.CONSUMER_KEY,
                                        self.settings.CONSUMER_SECRET)
        self.auth.set_access_token(self.settings.ACCESS_TOKEN,
                                   self.settings.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.stream_listener = LokiStreamListener(self.api, self.filter_type)
        self.streaming_api = tweepy.streaming.Stream(self.auth,
                                                     self.stream_listener)

    def stream(self):
        """Starts the Twitter stream."""
        while True:
            try:
                if self.filter_type == 'location':
                    self.streaming_api.filter(locations=self.location)
                elif self.filter_type == 'keyword':
                    self.streaming_api.filter(track=self.keywords)
            except (Exception, SystemExit) as e:
                print('Exception occured: {}'.format(e))
