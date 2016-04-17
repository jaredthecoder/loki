#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_streamer.py
"""


import pickle
import sys

import redis as redis_cls


__author__ = 'Jared M Smith'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jared M Smith'
__email__ = 'jared@jaredsmith.io'


def main():

    r = redis_cls.StrictRedis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe('loki01')

    try:
        while True:
            with open('sample_data.txt', 'r') as f:
                for line in f:
                    json_data = line.rstrip()
                    if not json_data:
                        continue
                    r.publish('loki01', pickle.dumps(json_data))
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()