#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

from datetime import datetime

import pytest

from mongo_queries_manager import mqm


_PYTEST_HAS_DATEPARSER: bool
try:
    import dateparser  # nopycln: import # noqa: F401

    _PYTEST_HAS_DATEPARSER = True
except ModuleNotFoundError:
    _PYTEST_HAS_DATEPARSER = False


@pytest.mark.skipif(
    _PYTEST_HAS_DATEPARSER is False,
    reason="Test skipped because dateparser isn't install.",
)
def test_datetime_query_with_dateparser_lib() -> None:
    query_result = mqm(string_query="date=2022-10-29", blacklist=[])

    assert query_result == {
        "filter": {"date": datetime(2022, 10, 29, 0, 0, 0, 0)},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }


@pytest.mark.skipif(
    _PYTEST_HAS_DATEPARSER is True, reason="Test skipped because dateparser is install."
)
def test_datetime_query_without_dateparser_lib() -> None:
    query_result = mqm(string_query="date=2022-10-29 ", blacklist=[])

    assert query_result == {
        "filter": {"date": "2022-10-29 "},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }


def test_datetime_query_with_a_datetime_format() -> None:
    query_result = mqm(string_query="date=2022-10-29T12:42:07.092062", blacklist=[])

    assert query_result == {
        "filter": {"date": datetime.fromisoformat("2022-10-29T12:42:07.092062")},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }
