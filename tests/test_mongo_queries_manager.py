#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest

from mongo_queries_manager import mqm, ListOperatorError, FilterError

# "status=sent&toto=true&timestamp>2016-01-01&author.firstName=/john/i&limit=100&skip=50&sort=-timestamp"


def test_empty_url_query():
    query_result = mqm(string_query="")

    assert query_result == {'filter': {}, 'sort': None, 'skip': 0, 'limit': 0}


def test_list_operator_error():
    with pytest.raises(ListOperatorError) as excinfo:
        query_result = mqm(string_query="flag<=toto,titi,tutu")

    assert excinfo.value.__str__() == 'List operator not found'


def test_filter_error():
    with pytest.raises(FilterError) as excinfo:
        query_result = mqm(string_query="flag==toto")

    assert excinfo.value.__str__() == 'Fail to split filter flag==toto with operator ='


def test_operator_error():
    with pytest.raises(FilterError) as excinfo:
        query_result = mqm(string_query="flag==toto")

    assert excinfo.value.__str__() == 'Fail to split filter flag==toto with operator ='
