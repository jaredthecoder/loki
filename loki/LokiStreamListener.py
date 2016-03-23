# -*- coding: utf-8 -*-

""" LokiStreamListener.py

Class for the custom stream listener passed to Tweepy
"""


# Python standard library assets
import json
import pickle
import sys

# 3rd Party assets
import redis
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
    def __init__(self, api, filter_type, args, logger=None):
        self.cli_args = args
        self.api = api
        self.filter_type = filter_type
        self.logger = logger
        self.statistics = cli.statistics
        self.redis = cli.redis
        self.analyzer = None
        if self.redis:
            self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
            self.p = self.r.pubsub()
            self.p.subscribe(self.cli_args.redis_channel)

        super(tweepy.StreamListener, self).__init__()

    def on_status(self, status):

        data = dict()
        if status.coordinates is not None \
                and status.coordinates['type'] == 'Point':
            log_if_exists(self.logger, 'Status Text: {}'.format(status.text), 'DEBUG')

            data['text'] = status.text
            data['lon'] = status.coordinates['coordinates'][0]
            data['lat'] = status.coordinates['coordinates'][1]
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

            json_data = json.dumps(data)
            # self.r.set(data['id_str'], json_data)
            if self.redis:
                self.r.publish(self.cli_args.redis_channel, pickle.dumps(json_data))

    # Execute on error
    def on_error(self, status_code):
        print('Encountered error with status code: {}'.format(status_code),
              file=sys.stderr)
        return True  # Don't kill the stream

    # Execute on timeout
    def on_timeout(self):
        print('Timeout occurred on stream.', file=sys.stderr)
        return True  # Don't kill the stream
