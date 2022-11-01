#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

from datetime import datetime

from mongo_queries_manager import mqm


def test_simple_range_support() -> None:
    query_result = mqm(string_query="user_id>525&user_id<600", blacklist=[])

    assert query_result == {
        "filter": {"user_id": {"$gt": 525, "$lt": 600}},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }


def test_simple_range_support_bis() -> None:
    query_result = mqm(
        string_query="user_id>525&user_id<600&creation_date>=2022-10-29T00:00:00.000000&"
        "creation_date<=2022-10-30T00:00:00.000000",
        blacklist=["latitude", "longitude"],
    )

    assert query_result == {
        "filter": {
            "user_id": {"$gt": 525, "$lt": 600},
            "creation_date": {
                "$gte": datetime.fromisoformat("2022-10-29T00:00:00.000000"),
                "$lte": datetime.fromisoformat("2022-10-30T00:00:00.000000"),
            },
        },
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }
