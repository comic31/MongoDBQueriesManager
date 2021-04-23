#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest

from mongo_queries_manager import mqm


class TestPopulation:
    def test_empty_population(self):
        query_result = mqm(string_query="populate=")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    def test_simple_population(self):
        query_result = mqm(string_query="populate=user")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': None, 'population': [{'path': 'user', 'projection': None}]}

    def test_multi_population(self):
        query_result = mqm(string_query="populate=user,settings")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': None, 'population': [{'path': 'user', 'projection': None},
                                                                   {'path': 'settings', 'projection': None}]}

    def test_simple_population_with_projection(self):
        query_result = mqm(string_query="fields=-created_at,-updated_at,hives.label&populate=hives")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': {'created_at': 0, 'updated_at': 0},
                                'population': [{'path': 'hives', 'projection': {'label': 1}}]}

    def test_multi_population_with_multi_projection(self):
        query_result = mqm(string_query="fields=-created_at,-updated_at,hives.label,hives._id,"
                                        "data.temperature&populate=hives,data")

        assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': {'created_at': 0, 'updated_at': 0},
                                'population': [{'path': 'hives', 'projection': {'label': 1, '_id': 1}},
                                               {'path': 'data', 'projection': {'temperature': 1}}]}
