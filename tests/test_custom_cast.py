#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

from typing import List

import pytest

from mongo_queries_manager import mqm, CustomCasterFail


class TestCustomCast:
    # Test good custom type
    def test_custom_cast(self):
        query_result = mqm(string_query="price=string(5)", casters={'string': str})

        assert query_result == {'filter': {'price': '5'}, 'sort': None, 'skip': 0, 'limit': 0,
                                'projection': None, 'population': [],}

    def test_custom_cast_2(self):

        def parse_custom_list(custom_list: str) -> List[str]:
            return custom_list.split(';')

        query_result = mqm(string_query="price=string(5)&name=John&in_stock=custom_list(1;2;3;4)&"
                                        "in_stock_string=custom_list(string(1);string(2);string(3);string(4))",
                           casters={'string': str, 'custom_list': parse_custom_list})

        assert query_result == {'filter': {'price': '5', 'name': 'John',
                                           'in_stock': {'$in': [1, 2, 3, 4]},
                                           'in_stock_string': {'$in': ['1', '2', '3', '4']}},
                                'sort': None, 'skip': 0, 'limit': 0, 'projection': None, 'population': []}

    # Test bad custom type
    def test_custom_cast_fail(self):

        with pytest.raises(CustomCasterFail) as excinfo:
            query_result = mqm(string_query="price=float(A.B)", casters={'float': float})

        assert excinfo.value.__str__() == 'Fail to cast float(A.B) with caster float'
