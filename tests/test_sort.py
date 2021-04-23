#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest
import pymongo

from mongo_queries_manager import mqm


class TestSort:
    # Sort good tests part
    def test_empty_sort(self):
        query_result = mqm(string_query="sort=")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_simple_ascending_sort(self):
        query_result = mqm(string_query="sort=_id")

        assert query_result == {'filter': {}, 'sort': [('_id', pymongo.ASCENDING)],
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_simple_ascending_sort_2(self):
        query_result = mqm(string_query="sort=+_id")

        assert query_result == {'filter': {}, 'sort': [('_id', pymongo.ASCENDING)],
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_simple_descending_sort(self):
        query_result = mqm(string_query="sort=-_id")

        assert query_result == {'filter': {}, 'sort': [('_id', pymongo.DESCENDING)],
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_multi_ascending_sort(self):
        query_result = mqm(string_query="sort=_id,created_at,price")

        assert query_result == {'filter': {}, 'sort': [('_id', pymongo.ASCENDING),
                                                       ('created_at', pymongo.ASCENDING),
                                                       ('price', pymongo.ASCENDING)],
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_multi_descending_sort(self):
        query_result = mqm(string_query="sort=-_id,-created_at,-price")

        assert query_result == {'filter': {}, 'sort': [('_id', pymongo.DESCENDING),
                                                       ('created_at', pymongo.DESCENDING),
                                                       ('price', pymongo.DESCENDING)],
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_multi_mixed_sort(self):
        query_result = mqm(string_query="sort=_id,-created_at,price,-active")

        assert query_result == {'filter': {}, 'sort': [('_id', pymongo.ASCENDING),
                                                       ('created_at', pymongo.DESCENDING),
                                                       ('price', pymongo.ASCENDING),
                                                       ('active', pymongo.DESCENDING)],
                                'skip': 0, 'limit': 0, 'projection': None, 'population': []}
