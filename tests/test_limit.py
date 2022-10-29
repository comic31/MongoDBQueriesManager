#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

import pytest

from mongo_queries_manager import LimitError, mqm


class TestLimit:
    # Limit good tests part
    def test_good_limit(self) -> None:
        query_result = mqm(string_query="limit=5")

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 5,
            "projection": None,
        }

    def test_empty_limit(self) -> None:
        query_result = mqm(string_query="limit=")

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Limit bad tests part
    def test_bad_limit_neg(self) -> None:
        with pytest.raises(LimitError) as excinfo:
            _ = mqm(string_query="limit=-5")

        assert excinfo.value.__str__() == "Negative limit value"

    def test_bad_limit_invalid_value(self) -> None:
        with pytest.raises(LimitError) as excinfo:
            _ = mqm(string_query="limit=toto")

        assert excinfo.value.__str__() == "Bad limit value"
