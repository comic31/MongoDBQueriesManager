#!/usr/bin/env python3
# Copyright (c) Dangla Théo, 2026

"""MongoDBQueriesManager helpers functions."""

__all__ = ["is_blacklisted_value"]

from typing import Any

from mongo_queries_manager.mongodb_queries_manager import MongoDBQueriesManager


def is_blacklisted_value(blacklist: list[str], arg: str) -> bool:
    """Check if a value is blacklisted.

    Args:
        blacklist (list[str]): Filter on all keys except the ones specified.
        arg (str): Argument to check.

    Returns:
        bool: True if the value is blacklisted, False otherwise.
    """
    return any(arg.startswith(f"{blacklist}=") for blacklist in blacklist)


def parse_query_operation(
    mongodb_query: dict[str, Any], arg: str, mongodb_queries_mgr: MongoDBQueriesManager, populate: bool
) -> dict[str, Any]:
    """Parse query operation into mongodb query.

    Args:
        mongodb_query (dict[str, Any]): Filter on all keys except the ones specified.
        arg (str): Query operation argument to convert.
        mongodb_queries_mgr: MongoDBQueriesManager object.
        populate (bool): True if the query need to be populated, False otherwise.

    Returns:
        bool: True if the value is blacklisted, False otherwise.
    """
    if arg.startswith("populate="):
        # Return directly to avoid population parsing issues.
        return mongodb_query
    elif arg.startswith("sort="):
        mongodb_query["sort"] = mongodb_queries_mgr.sort_logic(sort_params=arg)
    elif arg.startswith("limit="):
        mongodb_query["limit"] = mongodb_queries_mgr.limit_logic(limit_param=arg)
    elif arg.startswith("skip="):
        mongodb_query["skip"] = mongodb_queries_mgr.skip_logic(skip_param=arg)
    elif arg.startswith("fields="):
        if not populate:
            mongodb_query["projection"] = mongodb_queries_mgr.projection_logic(projection_param=arg, population=None)
            return mongodb_query

        mongodb_query["projection"] = mongodb_queries_mgr.projection_logic(
            projection_param=arg, population=mongodb_query["population"]
        )

    elif arg.startswith("$text="):
        mongodb_query["filter"] = {
            **mongodb_query["filter"],
            "$text": {"$search": mongodb_queries_mgr.text_operator_logic(text_param=arg)},
        }
    elif arg != "":
        for key, sub_filter in mongodb_queries_mgr.filter_logic(filter_params=arg).items():
            if key not in mongodb_query["filter"]:
                mongodb_query["filter"][key] = sub_filter
                continue

            mongodb_query["filter"][key] = {
                **mongodb_query["filter"][key],
                **sub_filter,
            }

    return mongodb_query
