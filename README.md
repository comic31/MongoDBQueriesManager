# MongoDBQueriesManager
[![Codecov](https://img.shields.io/codecov/c/github/comic31/MongoDBQueriesManager?style=for-the-badge)](https://app.codecov.io/gh/comic31/MongoDBQueriesManager)
[![Travis (.com)](https://img.shields.io/travis/com/comic31/MongoDBQueriesManager?style=for-the-badge)](https://travis-ci.com/github/comic31/MongoDBQueriesManager)
[![PyPI](https://img.shields.io/pypi/v/mongo-queries-manager?style=for-the-badge)](https://pypi.org/project/mongo-queries-manager/)
[![GitHub](https://img.shields.io/github/license/comic31/MongoDBQueriesManager?style=for-the-badge)](https://github.com/comic31/MongoDBQueriesManager/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mongo-queries-manager?style=for-the-badge)](https://pypi.org/project/mongo-queries-manager/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=for-the-badge)](https://github.com/comic31/MongoDBQueriesManager/blob/main/code_of_conduct.md)

Convert query parameters from API urls to MongoDB queries !

This project was inspired by [api-query-params](https://github.com/loris/api-query-params) (JS Library).

## Features:
- **Powerful**: Supports most of MongoDB operators ($in, $regexp, ...) and features (nested objects, type casting, projection...)
- **Agnostic**: Works with any web frameworks (Flask, Sanic, ...) and/or MongoDB libraries (pymongo, motor, ...)
- **Simple**: ~300 LOC, Python typing
- **Tested**: 100% code coverage

## Installation:
```shell script
pipenv install mongo-queries-manager
```

## Usages:
### Api
`mqm(string_query: str, casters: Optional[Dict[str, Callable]] = None) -> Dict[str, Any]`

##### Description
Converts `string_query` into a MongoDB query dict.

##### Arguments
- `string_query`: query string of the requested API URL (ie, `frist_name=John&limit=10`), Works with url encoded. [required]
- `casters`: Custom caster dict, used to define custom type (ie, `casters={'string': str}` / `price=string(5.5)` -> `{'price': '5'}`) [optional]

##### Returns
The resulting dictionary contains the following properties:
- `filter`: Contains the query criteria.
- `projection`: Contains the query projection
- `sort`: Contains the sort criteria (cursor modifiers).
- `skip`: Contains the skip criteria (cursor modifiers).
- `limit`:  Contains the limit criteria (cursor modifiers).

##### Exception
In case of error the following exception was raised:

- `MongoDBQueriesManagerBaseError`: Base MongoDBQueriesManager errors.
- `SkipError`: Raised when skip is negative / bad value.
- `LimitError`: Raised when limit is negative / bad value.
- `ListOperatorError`: Raised list operator was not possible.
- `FilterError`: Raised when parse filter method fail to find a valid match.
- `TextOperatorError`: Raised when parse text operator contain an empty string.
- `CustomCasterFail`: Raised when a custom cast fail.
- `ProjectionError`: Raised when projection json is invalid.

##### Examples:

**Simple demo**
```python
from mongo_queries_manager import mqm

mongodb_query = mqm(string_query="status=sent&price>=5.6&active=true&timestamp>"
                                 "2016-01-01&author.firstName=/john/i&limit=100&skip=50&sort=-timestamp&fields=-_id,-created_at")

#{
#   'filter':
#       {
#           'status': 'sent',
#           'price': {'$gte': 5.6},
#           'active': True,
#           'timestamp': {'$gt': datetime.datetime(2016, 1, 1, 0, 0)},
#           'author.firstName': re.compile('/john/i')
#       },
#   'projection': {'_id': 0, 'created_at': 0},
#   'sort': [('timestamp', -1)],
#   'skip': 50,
#   'limit': 100
#}
```

**Examples with PyMongo**
```python
from typing import Dict, Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from mongo_queries_manager import mqm

client: MongoClient = MongoClient('localhost', 27017)
db: Database = client['test-database']
collection: Collection = db['test-collection']

mongodb_query: Dict[str, Any] = mqm(string_query="status=sent&toto=true&timestamp>2016-01-01&"
                                 "author.firstName=/john/i&limit=100&skip=50&sort=-timestamp")

result = collection.find(**mongodb_query)
```

## Supported features

#### Filter operators:
| MongoDB   | URI                  | Example                 | Result                                                                        |
| :-------: | :------------------: | :---------------------: | :---------------------------------------------------------------------------: |
| `$eq`     | `key=val`            | `type=public`           | `{'filter': {'type': 'public'}}`                                              |
| `$gt`     | `key>val`            | `count>5`               | `{'filter': {'count': {'$gt': 5}}}`                                           |
| `$gte`    | `key>=val`           | `rating>=9.5`           | `{'filter': {'rating': {'$gte': 9.5}}}`                                       |
| `$lt`     | `key<val`            | `createdAt<2016-01-01`  | `{'filter': {'createdAt': {'$lt': datetime.datetime(2016, 1, 1, 0, 0)}}}`     |
| `$lte`    | `key<=val`           | `score<=-5`             | `{'filter': {'score': {'$lte': -5}}}`                                         |
| `$ne`     | `key!=val`           | `status!=success`       | `{'filter': {'status': {'$ne': 'success'}}}`                                  |
| `$in`     | `key=val1,val2`      | `country=GB,US`         | `{'filter': {'country': {'$in': ['GB', 'US']}}}`                              |
| `$nin`    | `key!=val1,val2`     | `lang!=fr,en`           | `{'filter': {'lang': {'$nin': ['fr', 'en']}}}`                                |
| `$exists` | `key`                | `phone`                 | `{'filter': {'phone': {'$exists': True}}}`                                    |
| `$exists` | `!key`               | `!email`                | `{'filter': {'email': {'$exists': False}}}`                                   |
| `$regex`  | `key=/value/<opts>`  | `email=/@gmail\.com$/i` | `{'filter': {'email': re.compile('/@gmail.com$/i')}}`                         |
| `$regex`  | `key!=/value/<opts>` | `phone!=/^06/`          | `{'filter': {'phone': { '$not': re.compile('/^06/')}}}`                       |
| `$text`   | `$text=val`          | `$text=toto -java`      | `{'filter': {'$text': { '$search': 'toto -java'}}}`                             |
| `$text`   | `$text=val`          | `$text="toto"`          | `{'filter': {'$text': { '$search': '"toto"'}}}`                             |

#### Skip / Limit operators:

- Default operator keys are `skip` and `limit`.
- Used to limit the number of records returned by the query (pagination, result limitation, ...).
- Support empty value (ie, `...&skip=&...` / `...&limit=&...` ).

```python
from typing import Dict, Any

from mongo_queries_manager import mqm

mongodb_query: Dict[str, Any] = mqm(string_query="skip=50&limit=50")
#{
#   'filter': {},
#   'sort': None,
#   'projection': None,
#   'skip': 50,
#   'limit': 50
#}

mongodb_query: Dict[str, Any] = mqm(string_query="skip=&limit=")
#{
#   'filter': {},
#   'sort': None,
#   'projection': None,
#   'skip': 0,
#   'limit': 0
#}
```

#### Sort operator:
- Used to sort returned records.
- Default operator key is `sort`.
- Support empty value (ie, `...&sort=&...`).
- Sort accepts a comma-separated list of fields. 
- Default behavior is to sort in ascending order. 
- Use `-` prefixes to sort in descending order, use `+` prefixes to sort in ascending order.

```python
from typing import Dict, Any

from mongo_queries_manager import mqm

mongodb_query: Dict[str, Any] = mqm(string_query="sort=created_at,-_id,+price")
#{
#   'filter': {},
#   'sort': [('created_at', 1), ('_id', -1), ('price', 1)],
#   'projection': None,
#   'skip': 0,
#   'limit': 0
#}
```

#### Projection operator:
- Useful to limit fields to return in each records.
- It accepts a comma-separated list of fields. Default behavior is to specify fields to return. Use - prefixes to return all fields except some specific fields.
- Due to a MongoDB limitation, you cannot combine inclusion and exclusion semantics in a single projection with the exception of the _id field.
- It also accepts JSON string to use more powerful projection operators ($, $elemMatch or $slice)

```python
from typing import Dict, Any

from mongo_queries_manager import mqm

mongodb_query: Dict[str, Any] = mqm(string_query="fields=-_id,-price")
#{
#   'filter': {},
#   'sort': None,
#   'projection': {'_id': 0, 'price': 0},
#   'skip': 0,
#   'limit': 0
#}


mongodb_query: Dict[str, Any] = mqm(string_query="fields=_id,price")

#{
#   'filter': {},
#   'sort': None,
#   'projection': {'_id': 1, 'price': 1},
#   'skip': 0,
#   'limit': 0
#}


mongodb_query: Dict[str, Any] = mqm(string_query='fields={"games": {"$elemMatch":{"score": {"$gt": 5}}}},joined,lastLogin')

#{
#   'filter': {},
#   'sort': None,
#   'projection': {'games': {'$elemMatch': {'score': {'$gt': 5}}}, 'joined': 1, 'lastLogin': 1}},
#   'skip': 0,
#   'limit': 0
#}
```

#### Custom caster:
- Used to define custom type
- Optional parameter

```python
from typing import Dict, Any, List

from mongo_queries_manager import mqm

def parse_custom_list(custom_list: str) -> List[str]:
        return custom_list.split(';')

query_result: Dict[str, Any] = mqm(string_query="price=string(5)&name=John&in_stock=custom_list(1;2;3;4)&"
                                    "in_stock_string=custom_list(string(1);string(2);string(3);string(4))", 
                                    casters={'string': str, 'custom_list': parse_custom_list})

#{
# 'filter':
# {
#   'price': '5',
#   'name': 'John',
#   'in_stock': {'$in': [1, 2, 3, 4]},
#   'in_stock_string': {'$in': ['1', '2', '3', '4']}
#   },
#   'sort': None,
#   'projection': None,
#   'skip': 0,
#   'limit': 0
#}
```