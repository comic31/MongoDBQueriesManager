#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

import pytest

from mongo_queries_manager import FilterError, ListOperatorError, mqm


def test_empty_url_query() -> None:
    query_result = mqm(string_query="")

    assert query_result == {
        "filter": {},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }


def test_list_operator_error() -> None:
    with pytest.raises(ListOperatorError) as excinfo:
        _ = mqm(string_query="flag<=toto,titi,tutu")

    assert excinfo.value.__str__() == "List operator not found"


def test_filter_error() -> None:
    with pytest.raises(FilterError) as excinfo:
        _ = mqm(string_query="flag==toto")

    assert excinfo.value.__str__() == "Fail to split filter flag==toto with operator ="


def test_operator_error() -> None:
    with pytest.raises(FilterError) as excinfo:
        _ = mqm(string_query="flag==toto")

    assert excinfo.value.__str__() == "Fail to split filter flag==toto with operator ="
