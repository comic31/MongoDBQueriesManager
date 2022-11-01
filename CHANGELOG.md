# Changelog

## 1.0.0
* Added:
    - Support range filter
* Changed:
    - `dateparser` is now an extra dependencies
    - As default without `dateparser` extra, mongo_queries_manager cast only isoformat string into datetime
    - Use Poetry instead of pipenv
    - Use nox instead of tox
    - Update pyproject.toml
    - Add GitHub workflow (format, lint, type, test, coverage)
    - Add GitHub stale
    - Add pre-commit, black, isort, flake8 dev dependencies

## 0.2.1
* Fixed:
    - Regex issue on list format with space

## 0.2.0
* Added:
    - New exception `LogicalPopulationError` & `LogicalSubPopulationError`
    - New population & projection tests
* Changed:
    - Clean docstrings
    - Population logic (use recursion)
    - Population projection logic (use recursion)

## 0.1.9
* Added:
    - Blacklist logic
    - Tests on blacklist logic

## 0.1.8
* Changed:
    - Population is now optional (default False)
* Changed:
    - Tests, fix population into dict returns (optional)

## 0.1.7
* Added:
    - Population logic with projection
    - Population tests
* Changed:
    - Tests, add Population into dict returns

## 0.1.6
* Added:
    - Mongo projection logic
    - Projection tests
    - New exception `ProjectionError`
* Changed:
    - Clean docstrings
    - Tests, add projection into dict returns

## 0.1.5
* Removed:
    - Regex logic for $text find
* Changed:
    - Text operator tests

## 0.1.4
* Added:
    - Mongo $text operator
    - New exception `TextOperatorError`
    - Text operator tests

## 0.1.2
* Added:
    - Custom cast
    - Custom cast tests

## 0.1.1
* Refactor:
    - Refactor class logic
    - Tests

## 0.1.0 (2021-02-12)
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
