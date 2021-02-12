#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

from urllib import parse
from typing import Dict, Any

from .mongodb_queries_manager import MongoDBQueriesManager, MongoDBQueriesManagerError

__version__ = "0.0.1"

__all__ = [
    'mqm',
    'MongoDBQueriesManagerError',
]


def mqm(string_query: str) -> Dict[str, Any]:
    try:
        args = [elem for elem in (parse.unquote(string_query)).split('&')]

        mongodb_query = {'filter': {},
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
    except Exception as err:
        raise MongoDBQueriesManagerError(raison=str(err))
    return mongodb_query
