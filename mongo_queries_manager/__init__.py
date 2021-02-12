#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

from typing import Dict, Any
from urllib import parse

from .mongodb_queries_manager import MongoDBQueriesManager, MongoDBQueriesManagerBaseError, SkipError, LimitError, \
    ListOperatorError, FilterError

__version__ = "0.1.0"

__all__ = [
    'mqm',
    'MongoDBQueriesManagerBaseError',
    'SkipError',
    'LimitError',
    'ListOperatorError',
    'FilterError',
]


def mqm(string_query: str) -> Dict[str, Any]:
    """ This method convert a string query into a MongoDB query dict.

    Args:
        string_query:

    Returns:

    """
    args = list(parse.unquote(string_query).split('&'))

    mongodb_query: Dict[str, Any] = {'filter': {},
                                     'sort': None,
                                     'skip': 0,
                                     'limit': 0,
                                     }

    for arg in args:
        if arg.startswith('sort='):
            mongodb_query['sort'] = MongoDBQueriesManager.sort_logic(sort_params=arg)
        elif arg.startswith('limit='):
            mongodb_query['limit'] = MongoDBQueriesManager.limit_logic(limit_param=arg)
        elif arg.startswith('skip='):
            mongodb_query['skip'] = MongoDBQueriesManager.skip_logic(skip_param=arg)
        elif arg != '':
            mongodb_query['filter'] = {**mongodb_query['filter'],
                                       **MongoDBQueriesManager.filter_logic(filter_params=arg)}

    return mongodb_query
