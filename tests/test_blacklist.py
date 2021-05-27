#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest

from mongo_queries_manager import mqm, ListOperatorError, FilterError

# "status=sent&toto=true&timestamp>2016-01-01&author.firstName=/john/i&limit=100&skip=50&sort=-timestamp"


def test_empty_blacklist_query():
    query_result = mqm(string_query="status=5", blacklist=[])

    assert query_result == {'filter': {"status": 5}, 'sort': None, 'skip': 0, 'limit': 0,
                            'projection': None}


def test_blacklist_query():
    query_result = mqm(string_query="status=5&latitude=43.6046256&longitude=1.444205",
                       blacklist=['latitude', 'longitude'])

    assert query_result == {'filter': {"status": 5}, 'sort': None, 'skip': 0, 'limit': 0,
                            'projection': None}
