#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

""" MongoDBQueriesManager """

from __future__ import annotations

from typing import Any, Callable
from urllib import parse

from mongo_queries_manager.mongodb_queries_manager import (
    CustomCasterFail,
    FilterError,
    LimitError,
    ListOperatorError,
    LogicalPopulationError,
    LogicalSubPopulationError,
    MongoDBQueriesManager,
    MongoDBQueriesManagerBaseError,
    ProjectionError,
    SkipError,
    TextOperatorError,
)


__version__ = "0.2.2"

__all__ = [
    "mqm",
    "MongoDBQueriesManagerBaseError",
    "SkipError",
    "LimitError",
    "ListOperatorError",
    "FilterError",
    "CustomCasterFail",
    "TextOperatorError",
    "ProjectionError",
    "LogicalPopulationError",
    "LogicalSubPopulationError",
]


def _sort_population(populate: str) -> int:
    """Used to sort population list by level (.) into populate value.

    Args:
        populate (str): Populate value.

    Returns:
        int: Return the number of . (level) into populate value.
    """
    return populate.count(".")


def mqm(
    string_query: str,
    blacklist: list[str] | None = None,
    casters: dict[str, Callable[[Any], Any]] | None = None,
    populate: bool = False,
) -> dict[str, Any]:
    """This method convert a string query into a MongoDB query dict.

    Args:
        string_query (str): A query string of the requested API URL.
        blacklist (Optional[List[str]]): Filter on all keys except the ones specified.
        populate (bool): Add population into returned query (Manual implementation).
        casters (Optional[Dict[str, Callable]]): Custom caster dict, used to define custom type.

    Returns:
        Dict[str, Any]: Return a mongodb query in dict format.
    """
    args: list[str] = list(parse.unquote(string_query).split("&"))
    mongodb_queries_mgr: MongoDBQueriesManager = MongoDBQueriesManager(casters=casters)
    mongodb_query: dict[str, Any] = {
        "filter": {},
        "sort": None,
        "skip": 0,
        "limit": 0,
        "projection": None,
    }

    if populate:
        mongodb_query["population"] = []

        populates_values = []
        for arg in args:
            if arg.startswith("populate=") and arg != "populate=":
                populates_values = (
                    arg.split("=")[1].split(",")
                    if arg.split("=")[1].find(",") > 0
                    else [arg.split("=")[1]]
                )

        for populate_value in sorted(populates_values, key=_sort_population):
            mongodb_queries_mgr.format_populate_value(
                mongodb_query, population_value=populate_value
            )

    for arg in args:
        if blacklist:
            found: bool = False
            for blacklist_value in blacklist:
                if arg.startswith(f"{blacklist_value}="):
                    found = True
                    break
            if found:
                continue

        if arg.startswith("sort="):
            mongodb_query["sort"] = mongodb_queries_mgr.sort_logic(sort_params=arg)
        elif arg.startswith("limit="):
            mongodb_query["limit"] = mongodb_queries_mgr.limit_logic(limit_param=arg)
        elif arg.startswith("skip="):
            mongodb_query["skip"] = mongodb_queries_mgr.skip_logic(skip_param=arg)
        elif arg.startswith("fields="):
            if populate:
                mongodb_query["projection"] = mongodb_queries_mgr.projection_logic(
                    projection_param=arg, population=mongodb_query["population"]
                )
            else:
                mongodb_query["projection"] = mongodb_queries_mgr.projection_logic(
                    projection_param=arg, population=None
                )
        elif arg.startswith("$text="):
            mongodb_query["filter"] = {
                **mongodb_query["filter"],
                "$text": {
                    "$search": mongodb_queries_mgr.text_operator_logic(text_param=arg)
                },
            }
        elif arg.startswith("populate="):
            pass
        elif arg != "":
            for key, sub_filter in mongodb_queries_mgr.filter_logic(
                filter_params=arg
            ).items():
                if key in mongodb_query["filter"]:
                    mongodb_query["filter"][key] = {
                        **mongodb_query["filter"][key],
                        **sub_filter,
                    }
                else:
                    mongodb_query["filter"][key] = sub_filter

    return mongodb_query
