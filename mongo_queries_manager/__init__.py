#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

from typing import Dict, Any, Callable, Optional, List
from urllib import parse

from .mongodb_queries_manager import MongoDBQueriesManager, MongoDBQueriesManagerBaseError, SkipError, LimitError, \
    ListOperatorError, FilterError, CustomCasterFail, TextOperatorError, ProjectionError

__version__ = "0.1.6"

__all__ = [
    'mqm',
    'MongoDBQueriesManagerBaseError',
    'SkipError',
    'LimitError',
    'ListOperatorError',
    'FilterError',
    'CustomCasterFail',
    'TextOperatorError',
    'ProjectionError'
]


def mqm(string_query: str, casters: Optional[Dict[str, Callable]] = None) -> Dict[str, Any]:
    """ This method convert a string query into a MongoDB query dict.

    Args:
        string_query (str): A query string of the requested API URL.
        casters (Optional[Dict[str, Callable]]): Custom caster dict, used to define custom type

    Returns:
        Dict[str, Any]: Return a mongodb query in dict format
    """
    args: List[str] = list(parse.unquote(string_query).split('&'))

    mongodb_queries_mgr: MongoDBQueriesManager = MongoDBQueriesManager(casters=casters)

    mongodb_query: Dict[str, Any] = {'filter': {},
                                     'sort': None,
                                     'projection': None,
                                     'skip': 0,
                                     'limit': 0,
                                     }

    for arg in args:
        if arg.startswith('sort='):
            mongodb_query['sort'] = mongodb_queries_mgr.sort_logic(sort_params=arg)
        elif arg.startswith('limit='):
            mongodb_query['limit'] = mongodb_queries_mgr.limit_logic(limit_param=arg)
        elif arg.startswith('skip='):
            mongodb_query['skip'] = mongodb_queries_mgr.skip_logic(skip_param=arg)
        elif arg.startswith('fields='):
            mongodb_query['projection'] = mongodb_queries_mgr.projection_logic(projection_param=arg)
        elif arg.startswith('$text='):
            mongodb_query['filter'] = \
                {**mongodb_query['filter'],
                 **{'$text': {'$search': mongodb_queries_mgr.text_operator_logic(text_param=arg)}}}
        elif arg.startswith('populate='):
            pass
        elif arg != '':
            mongodb_query['filter'] = {**mongodb_query['filter'],
                                       **mongodb_queries_mgr.filter_logic(filter_params=arg)}

    return mongodb_query
