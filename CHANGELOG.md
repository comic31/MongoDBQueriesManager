# Changelog

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