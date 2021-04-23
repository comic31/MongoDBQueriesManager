#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import re
from mongo_queries_manager import mqm


class TestBasicOperator:
    # Operator equal tests part (=)
    def test_operator_equal(self):
        query_result = mqm(string_query="status=5")

        assert query_result == {'filter': {"status": 5}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': None}

    # Operator different than tests part (!=)
    def test_operator_different_than(self):
        query_result = mqm(string_query="count!=5")

        assert query_result == {'filter': {"count": {"$ne": 5}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None}

    # Operator superior tests part (>)
    def test_operator_superior(self):
        query_result = mqm(string_query="count>5")

        assert query_result == {'filter': {"count": {"$gt": 5}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None}

    # Operator inferior tests part (<)
    def test_operator_inferior(self):
        query_result = mqm(string_query="count<5")

        assert query_result == {'filter': {"count": {"$lt": 5}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None}

    # Operator superior or equal tests part (>=)
    def test_operator_superior_or_equal(self):
        query_result = mqm(string_query="count>=5")

        assert query_result == {'filter': {"count": {"$gte": 5}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None}

    # Operator inferior or equal tests part (<=)
    def test_operator_inferior_or_equal(self):
        query_result = mqm(string_query="count<=5")

        assert query_result == {'filter': {"count": {"$lte": 5}}, 'sort': None,
                                'skip': 0, 'limit': 0, 'projection': None}

    # Operator in tests part (=)
    def test_operator_in(self):
        query_result = mqm(string_query="country=GB,US")

        assert query_result == {'filter': {"country": {"$in": ['GB', 'US']}},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None}

    # Operator not in tests part (!=)
    def test_operator_not_in(self):
        query_result = mqm(string_query="country!=GB,US")

        assert query_result == {'filter': {"country": {"$nin": ['GB', 'US']}},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None}

    # Operator exists tests part (!=)
    def test_operator_exists(self):
        query_result = mqm(string_query="phone")

        assert query_result == {'filter': {"phone": {"$exists": True}},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None}

    # Operator exists tests part (!=)
    def test_operator_not_exists(self):
        query_result = mqm(string_query="!phone")

        assert query_result == {'filter': {"phone": {"$exists": False}},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None}

    # Operator regex equal tests part (=)
    def test_operator_regex(self):
        query_result = mqm(string_query="email=/@gmail\\.com$/i")

        assert query_result == {'filter': {"email": re.compile(r'/@gmail\.com$/i')},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None}

    # Operator regex equal tests part (!=)
    def test_operator_different_than_regex(self):
        query_result = mqm(string_query="email!=/@gmail\\.com$/i")

        assert query_result == {'filter': {"email": {"$ne": re.compile(r'/@gmail\.com$/i')}},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None}
