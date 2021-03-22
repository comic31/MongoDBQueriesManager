#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import pytest

from mongo_queries_manager import mqm, TextOperatorError


class TestTextOperator:
    # Text operator good tests part
    def test_good_text_operator(self):
        query_result = mqm(string_query="$text=toto")

        assert query_result == {'filter': {'$text': {'$search': 'toto'}}, 'sort': None, 'skip': 0, 'limit': 0}

    def test_good_text_operator2(self):
        query_result = mqm(string_query='$text="toto"')

        assert query_result == {'filter': {'$text': {'$search': '"toto"'}}, 'sort': None, 'skip': 0, 'limit': 0}

    # Skip bad tests part
    def test_empty_test_operator(self):
        with pytest.raises(TextOperatorError) as excinfo:
            query_result = mqm(string_query="$text=")

        assert excinfo.value.__str__() == 'Bad $text value'
