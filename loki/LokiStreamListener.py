# -*- coding: utf-8 -*-

""" LokiStreamListener.py

Class for the custom stream listener passed to Tweepy
"""


# Python standard library assets
import json
import pickle
import sqlite3

# 3rd Party assets
import tweepy

# Project assets
from loki.utils import log_if_exists


__author__ = 'Jared M Smith'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jared M Smith'
__email__ = 'jared@jaredsmith.io'


# Embedded class for the stream listener that
# will pull from the Twitter Streaming API
class LokiStreamListener(tweepy.StreamListener):

    # Initialize the class
    def __init__(self, api, args, logger=None):
        self.api = api
        self.cli_args = args
        self.logger = logger

        self.filter_type = self.cli_args.filter_type
        self.statistics = self.cli_args.statistics
        self.redis = self.cli_args.redis
        self.location_only = self.cli_args.location_only
        self.analyzer = None
        self.sql_db_path = self.cli_args.sql_db_path
        self.sql_db_conn = sqlite3.connect(self.sql_db_path)
        self.sql_db_curs = self.sql_db_conn.cursor()

        if self.redis:
            import redis as redis_cls
            self.r = redis_cls.StrictRedis(host='localhost', port=6379, db=0)
            self.p = self.r.pubsub()
            self.p.subscribe(self.cli_args.redis_channel)

        super(tweepy.StreamListener, self).__init__()

    def on_status(self, status):

        location_exists = False
        status_counter = 0

        data = dict()

        log_if_exists(self.logger, 'Status Text: {}'.format(status.text),
                      'DEBUG')

        data['text'] = status.text
        data['user_location_str'] = status.user.location
        data['location_place_name'] = status.place.name
        data['location_place_full_name'] = status.place.full_name
        data['location_place_country'] = status.place.country
        data['location_place_country_code'] = status.place.country_code
        data['location_place_type'] = status.place.place_type
        data['user_time_zone'] = status.user.time_zone
        data['source'] = status.source
        data['source_url'] = status.source_url
        data['id_str'] = status.id_str
        data['user_profile_image_url'] = status.user.profile_image_url
        data['user_profile_background_image_url'] = \
            status.user.profile_background_image_url
        data['user_screen_name'] = status.user.screen_name
        data['user_status_count'] = status.user.statuses_count
        data['user_followers_count'] = status.user.followers_count
        data['user_friends_count'] = status.user.friends_count
        data['user_favourites_count'] = status.user.favourites_count
        data['user_url'] = status.user.url
        data['user_description'] = status.user.description
        data['user_id_str'] = status.user.id_str
        data['language_code'] = status.lang
        data['created_at'] = \
            status.created_at.strftime("%a, %d %b %Y %H:%M:%S +0000")

        if status.coordinates is not None \
                and status.coordinates['type'] == 'Point':

            data['lon'] = status.coordinates['coordinates'][0]
            data['lat'] = status.coordinates['coordinates'][1]

            location_exists = True

        json_data = json.dumps(data)
        # self.r.set(data['id_str'], json_data)

        if not self.location_only:
            if self.redis:
                self.r.publish(self.cli_args.redis_channel,
                               pickle.dumps(json_data))
        elif self.location_only and location_exists:
            if self.redis:
                self.r.publish(self.cli_args.redis_channel,
                               pickle.dumps(json_data))

    # Execute on error
    def on_error(self, status_code):
        log_if_exists(self.logger,
                      'Encountered error with status code: {}'.format(
                          status_code),
                      'ERROR')
        return True  # Don't kill the stream

    # Execute on timeout
    def on_timeout(self):
        log_if_exists(self.logger,
                      'Timeout occurred on stream.',
                      'WARNING')
        return True  # Don't kill the stream
