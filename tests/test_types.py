#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

import re

from datetime import datetime, timezone

from mongo_queries_manager import mqm


class TestTypes:
    # Type string tests part
    def test_type_string(self) -> None:
        query_result = mqm(string_query="name=toto")

        assert query_result == {
            "filter": {"name": "toto"},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type integer tests part
    def test_type_integer(self) -> None:
        query_result = mqm(string_query="price=5")

        assert query_result == {
            "filter": {"price": 5},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    def test_type_negative_integer(self) -> None:
        query_result = mqm(string_query="price=-5")

        assert query_result == {
            "filter": {"price": -5},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type float tests part
    def test_type_float(self) -> None:
        query_result = mqm(string_query="price=5.5")

        assert query_result == {
            "filter": {"price": 5.5},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    def test_type_negative_float(self) -> None:
        query_result = mqm(string_query="price=-5.5")

        assert query_result == {
            "filter": {"price": -5.5},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type datetime tests part
    def test_type_datetime_format_1(self) -> None:
        query_result = mqm(string_query="created_at=2016-01-01")

        assert query_result == {
            "filter": {"created_at": datetime(year=2016, month=1, day=1)},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    def test_type_datetime_format_2(self) -> None:
        query_result = mqm(string_query="created_at=2016-01-01T00:00:00.000000+00:00")

        assert query_result == {
            "filter": {
                "created_at": datetime(year=2016, month=1, day=1, tzinfo=timezone.utc)
            },
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type list tests part
    def test_type_list(self) -> None:
        query_result = mqm(string_query="country=US,RU")

        assert query_result == {
            "filter": {"country": {"$in": ["US", "RU"]}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type regex tests part
    def test_type_regex(self) -> None:
        query_result = mqm(string_query="email=/@gmail\\.com$/i")

        assert query_result == {
            "filter": {"email": re.compile(r"/@gmail\.com$/i")},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type boolean tests part
    def test_type_boolean_true(self) -> None:
        query_result = mqm(string_query="active=true")
        assert query_result == {
            "filter": {"active": True},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

        query_result = mqm(string_query="active=True")
        assert query_result == {
            "filter": {"active": True},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    def test_type_boolean_false(self) -> None:
        query_result = mqm(string_query="active!=false")
        assert query_result == {
            "filter": {"active": {"$ne": False}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

        query_result = mqm(string_query="active!=False")
        assert query_result == {
            "filter": {"active": {"$ne": False}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Type null tests part
    def test_type_null(self) -> None:
        query_result = mqm(string_query="active!=null")
        assert query_result == {
            "filter": {"active": {"$ne": None}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

        query_result = mqm(string_query="active!=Null")
        assert query_result == {
            "filter": {"active": {"$ne": None}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

        query_result = mqm(string_query="active!=none")
        assert query_result == {
            "filter": {"active": {"$ne": None}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

        query_result = mqm(string_query="active!=None")
        assert query_result == {
            "filter": {"active": {"$ne": None}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
