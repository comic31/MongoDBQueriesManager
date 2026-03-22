#!/usr/bin/env python3
# Copyright (c) Dangla Théo, 2026

"""MongoDBQueriesManager example with PyMongo."""

from __future__ import annotations

from typing import Any

from mongo_queries_manager import mqm
from pymongo import MongoClient

if __name__ == "__main__":
    client: MongoClient[dict[str, Any]] = MongoClient("localhost", 27017)
    db = client["test-database"]
    collection = db["test-collection"]

    mongodb_query = mqm(
        string_query=(
            "status=sent&toto=true&timestamp>2016-01-01&author.firstName=/john/i&limit=100&skip=50&sort=-timestamp"
        )
    )

    result = collection.find(**mongodb_query)
