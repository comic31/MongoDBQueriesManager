#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import re
from typing import Dict, Any, Optional, Tuple, List

import pymongo
from dateparser import parse


class MongoDBQueriesManagerError(AttributeError):
    def __init__(self, message: str = "Fail to build mongodb query", raison: str = ""):
        self.raison = raison
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} -> {self.raison}'


class MongoDBQueriesManager:
    mongodb_operator: Dict[str, str] = {
        '=': '$eq',
        '!=': '$ne',
        '>': '$gt',
        '>=': '$gte',
        '<': '$lt',
        '<=': '$lte',
        '!': '$exists',
        '': '$exists'
    }

    regex_dict: Dict[str, Any] = {
        re.compile(r"^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"): lambda floating: float(floating),
        re.compile(r"^[-+]?\d+$"): lambda integer: int(integer),
        re.compile(r"^[12]\d{3}(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)(T|"
                   r" )?(([01][0-9]|2[0-3]):[0-5]\d(:[0-5]\d(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?)?$"):
            lambda date: parse(date, languages=['fr', 'en']),
        re.compile(r"^\w+(?=(,?,))(?:\1\w+)+$"): lambda list_value: list_value.split(','),
        re.compile(r"\/((?![*+?])(?:[^\r\n\[/\\]|\\.|\[(?:[^\r\n\]\\]|\\.)*\])+)"
                   r"\/((?:g(?:im?|mi?)?|i(?:gm?|mg?)?|m(?:gi?|ig?)?)?)"): lambda regex: re.compile(regex),
        "true": lambda boolean: True,
        "false": lambda boolean: False,
        "null": lambda none: None,
    }

    @classmethod
    def find_operator(cls, filter_params: str) -> str:
        if filter_params.find('<=') > -1:
            return '<='
        elif filter_params.find('>=') > -1:
            return '>='
        elif filter_params.find('!=') > -1:
            return '!='
        elif filter_params.find('=') > -1:
            return '='
        elif filter_params.find('>') > -1:
            return '>'
        elif filter_params.find('<') > -1:
            return '<'
        elif filter_params.find('!') > -1:
            return '!'
        else:
            return ''

    @classmethod
    def cast_value_logic(cls, value: str) -> Any:
        for regex, cast in cls.regex_dict.items():
            if isinstance(regex, re.Pattern):
                if regex.match(value):
                    return cast(value)
            else:
                if regex == value:
                    return cast(value)
        return value

    @classmethod
    def filter_logic(cls, filter_params: str) -> Dict[str, Any]:
        operator = cls.find_operator(filter_params=filter_params)

        key, value = filter_params.split(operator)

        value = cls.cast_value_logic(value)

        # $eq logic
        if not isinstance(value, list) and operator == '=':
            return {key: value}

        # $in, $nin, $exists logic
        if isinstance(value, list):
            if operator == '=':
                return {key: {"$in": value}}
            elif operator == '!=':
                return {key: {"$nin": value}}
            else:
                raise MongoDBQueriesManagerError(raison='List operator not found')

        # $gt, $gte, $lt, $lte, $ne, $exists logic
        if operator in ['<=', ">=", "<", ">", '', '!', '!=']:
            return {key: {cls.mongodb_operator[operator]: value}}

    @classmethod
    def sort_logic(cls, sort_params: str) -> Optional[List[Tuple]]:
        sort_params_final: List[Tuple] = list()
        key, value = sort_params.split('=')

        if value:
            for param in value.split(','):
                if param.startswith('+'):
                    sort_params_final.append((param[1:], pymongo.ASCENDING))
                elif param.startswith('-'):
                    sort_params_final.append((param[1:], pymongo.DESCENDING))
                else:
                    sort_params_final.append((param, pymongo.ASCENDING))
            return sort_params_final
        return None

    @classmethod
    def limit_logic(cls, limit_param: str) -> int:
        return int(limit_param.split('=')[1])

    @classmethod
    def skip_logic(cls, skip_param: str) -> int:
        return int(skip_param.split('=')[1])
