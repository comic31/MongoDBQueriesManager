# Changelog

## 0.0.2 (2021-02-12)
* Added:
    - Tests (Operators, types, sort, skip, limit, errors).
    - New custom exception (SkipError, LimitError, ListOperatorError, FilterError), inherit from MongoDBQueriesManagerBaseError.
    - Limit now support empty value (ie, `limit=`).
    - Skip now support empty value (ie, `skip=`).
    - Code docstrings
* Changed:
    - Rename exception MongoDBQueriesManagerError to MongoDBQueriesManagerBaseError.
* Fix:
    - Issue with $exist operator.

## 0.0.1 (2021-02-12)
* Initial release.