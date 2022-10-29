#!/usr/bin/env python3
# Copyright (c) Modos Team, 2021

from __future__ import annotations

from typing import Any

from pymongo import MongoClient

from mongo_queries_manager import mqm


if __name__ == "__main__":
    client: MongoClient[dict[str, Any]] = MongoClient("localhost", 27017)
    db = client["test-database"]
    collection = db["test-collection"]

    mongodb_query = mqm(
        string_query=(
            "status=sent&toto=true&timestamp>2016-01-01&"
            "author.firstName=/john/i&limit=100&skip=50&sort=-timestamp"
        )
    )

    result = collection.find(**mongodb_query)
