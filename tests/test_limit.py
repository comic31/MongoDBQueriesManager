#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest

from mongo_queries_manager import mqm, LimitError


class TestLimit:
    # Limit good tests part
    def test_good_limit(self):
        query_result = mqm(string_query="limit=5")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 5, 'projection': None, 'population': []}

    def test_empty_limit(self):
        query_result = mqm(string_query="limit=")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Limit bad tests part
    def test_bad_limit_neg(self):
        with pytest.raises(LimitError) as excinfo:
            query_result = mqm(string_query="limit=-5")

        assert excinfo.value.__str__() == 'Negative limit value'

    def test_bad_limit_invalid_value(self):
        with pytest.raises(LimitError) as excinfo:
            query_result = mqm(string_query="limit=toto")

        assert excinfo.value.__str__() == 'Bad limit value'
