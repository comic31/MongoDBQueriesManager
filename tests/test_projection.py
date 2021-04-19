#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest

from mongo_queries_manager import mqm, ProjectionError


class TestProjection:
    def test_empty_projection(self):
        query_result = mqm(string_query="fields=")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0, 'projection': None}

    def test_simple_projection_1(self):
        query_result = mqm(string_query="fields=_id")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0, 'projection': {'_id': 1}}

    def test_simple_projection_2(self):
        query_result = mqm(string_query="fields=-_id")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0, 'projection': {'_id': 0}}

    def test_multi_projection_3(self):
        query_result = mqm(string_query="fields=_id,created_at,price")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': {'_id': 1, 'created_at': 1, 'price': 1}}

    def test_multi_projection_1(self):
        query_result = mqm(string_query="fields=-_id,-created_at,-price")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': {'_id': 0, 'created_at': 0, 'price': 0}}

    def test_complex_projection_1(self):
        query_result = mqm(string_query='fields={"games": {"$elemMatch":{"score": {"$gt": 5}}}},joined,lastLogin')

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': {'games': {'$elemMatch': {'score': {'$gt': 5}}},
                                               'joined': 1, 'lastLogin': 1}}

    def test_complex_projection_error(self):
        with pytest.raises(ProjectionError) as excinfo:
            query_result = mqm(string_query='fields={"games": {"$elemMatch":{"score": {"$gt": 5}}},joined,lastLogin')

        assert excinfo.value.__str__() == 'Fail to decode projection'
