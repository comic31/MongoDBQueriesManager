#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

from mongo_queries_manager import mqm


def test_empty_blacklist_query() -> None:
    query_result = mqm(string_query="status=5", blacklist=[])

    assert query_result == {
        "filter": {"status": 5},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }


def test_blacklist_query() -> None:
    query_result = mqm(
        string_query="status=5&latitude=43.6046256&longitude=1.444205",
        blacklist=["latitude", "longitude"],
    )

    assert query_result == {
        "filter": {"status": 5},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }
