#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2021

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

try:
    from mongodb_querie_manager import mqm
except ImportError:
    from src import mqm

if __name__ == '__main__':
    client: MongoClient = MongoClient('localhost', 27017)
    db: Database = client['test-database']
    collection: Collection = db['test-collection']

    mongodb_query = mqm(string_query="status=sent&toto=true&timestamp>2016-01-01&"
                                     "author.firstName=/john/i&limit=100&skip=50&sort=-timestamp")

    result = collection.find(**mongodb_query)
