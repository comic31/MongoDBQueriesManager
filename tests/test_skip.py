#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

import pytest

from mongo_queries_manager import SkipError, mqm


class TestSkip:
    # Skip good tests part
    def test_good_skip(self) -> None:
        query_result = mqm(string_query="skip=5")

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 5,
            "limit": 0,
            "projection": None,
        }

    def test_empty_skip(self) -> None:
        query_result = mqm(string_query="skip=")

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Skip bad tests part
    def test_bad_skip_neg(self) -> None:
        with pytest.raises(SkipError) as excinfo:
            _ = mqm(string_query="skip=-5")

        assert excinfo.value.__str__() == "Negative skip value"

    def test_bad_skip_invalid_value(self) -> None:
        with pytest.raises(SkipError) as excinfo:
            _ = mqm(string_query="skip=toto")

        assert excinfo.value.__str__() == "Bad skip value"
