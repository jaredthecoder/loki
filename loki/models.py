# -*- coding: utf-8 -*-

""" models.py

Database (PeeWee) models
"""

# Python standard library assets
import datetime

# 3rd Party Assets
from peewee import Model, BigIntegerField, CharField, FloatField, SqliteDatabase
from peewee import DateTimeField


__author__ = 'Jared M Smith'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jared M Smith'
__email__ = 'jared@jaredsmith.io'


db = None


def setup_db(name):
    db = SqliteDatabase(name)
    db.create_tables([Location, Statistics])


class Location(Model):

    # Human name for the location
    name = CharField()

    # Defines the bounding box of coordinates
    lat_north = FloatField()
    lat_south = FloatField()
    lon_east = FloatField()
    lon_west = FloatField()

    # Date Created
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class Statistics(Model):

    average = FloatField()
    total = BigIntegerField()
    rate_per_second = FloatField()
    rate_per_minute = FloatField()
    rate_per_hour = FloatField()

    class Meta:
        database = db

