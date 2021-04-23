#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import re
from datetime import datetime, timezone

from mongo_queries_manager import mqm


class TestTypes:
    # Type string tests part
    def test_type_string(self):
        query_result = mqm(string_query="name=toto")

        assert query_result == {'filter': {"name": 'toto'}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type integer tests part
    def test_type_integer(self):
        query_result = mqm(string_query="price=5")

        assert query_result == {'filter': {"price": 5}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_type_negative_integer(self):
        query_result = mqm(string_query="price=-5")

        assert query_result == {'filter': {"price": -5}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type float tests part
    def test_type_float(self):
        query_result = mqm(string_query="price=5.5")

        assert query_result == {'filter': {"price": 5.5}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_type_negative_float(self):
        query_result = mqm(string_query="price=-5.5")

        assert query_result == {'filter': {"price": -5.5}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type datetime tests part
    def test_type_datetime_format_1(self):
        query_result = mqm(string_query="created_at=2016-01-01")

        assert query_result == {'filter': {"created_at": datetime(year=2016, month=1, day=1)},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_type_datetime_format_2(self):
        query_result = mqm(string_query="created_at=2016-01-01T00:00:00.000000+00:00")

        assert query_result == {'filter': {"created_at": datetime(year=2016, month=1, day=1, tzinfo=timezone.utc)},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type list tests part
    def test_type_list(self):
        query_result = mqm(string_query="country=US,RU")

        assert query_result == {'filter': {"country": {"$in": ['US', 'RU']}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type regex tests part
    def test_type_regex(self):
        query_result = mqm(string_query="email=/@gmail\\.com$/i")

        assert query_result == {'filter': {"email": re.compile(r'/@gmail\.com$/i')}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type boolean tests part
    def test_type_boolean_true(self):
        query_result = mqm(string_query="active=true")
        assert query_result == {'filter': {"active": True}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': None, 'population': []}

        query_result = mqm(string_query="active=True")
        assert query_result == {'filter': {"active": True}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': None, 'population': []}

    def test_type_boolean_false(self):
        query_result = mqm(string_query="active!=false")
        assert query_result == {'filter': {"active": {'$ne': False}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

        query_result = mqm(string_query="active!=False")
        assert query_result == {'filter': {"active": {'$ne': False}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Type null tests part
    def test_type_null(self):
        query_result = mqm(string_query="active!=null")
        assert query_result == {'filter': {"active": {'$ne': None}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

        query_result = mqm(string_query="active!=Null")
        assert query_result == {'filter': {"active": {'$ne': None}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

        query_result = mqm(string_query="active!=none")
        assert query_result == {'filter': {"active": {'$ne': None}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

        query_result = mqm(string_query="active!=None")
        assert query_result == {'filter': {"active": {'$ne': None}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}
