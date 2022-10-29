#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

import pytest

from mongo_queries_manager import TextOperatorError, mqm


class TestTextOperator:
    # Text operator good tests part
    def test_good_text_operator(self) -> None:
        query_result = mqm(string_query="$text=toto")

        assert query_result == {
            "filter": {"$text": {"$search": "toto"}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    def test_good_text_operator2(self) -> None:
        query_result = mqm(string_query='$text="toto"')

        assert query_result == {
            "filter": {"$text": {"$search": '"toto"'}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }

    # Skip bad tests part
    def test_empty_test_operator(self) -> None:
        with pytest.raises(TextOperatorError) as excinfo:
            _ = mqm(string_query="$text=")

        assert excinfo.value.__str__() == "Bad $text value"
