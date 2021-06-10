#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import json
import re
from typing import Dict, Any, Optional, Tuple, List, Union, Callable

from dateparser import parse

ASCENDING = 1
"""Ascending sort order."""
DESCENDING = -1
"""Descending sort order."""


class MongoDBQueriesManagerBaseError(Exception):
    """ Base MongoDBQueriesManager errors. """


class SkipError(MongoDBQueriesManagerBaseError):
    """ Raised when skip is negative / bad value."""


class LimitError(MongoDBQueriesManagerBaseError):
    """ Raised when limit is negative / bad value. """


class ListOperatorError(MongoDBQueriesManagerBaseError):
    """ Raised list operator was not possible. """


class FilterError(MongoDBQueriesManagerBaseError):
    """ Raised when parse filter method fail to find a valid match. """


class TextOperatorError(MongoDBQueriesManagerBaseError):
    """ Raised when parse text operator contain an empty string. """


class CustomCasterFail(MongoDBQueriesManagerBaseError):
    """ Raised when a custom cast fail. """


class ProjectionError(MongoDBQueriesManagerBaseError):
    """ Raised when projection json is invalid. """


class LogicalPopulationError(MongoDBQueriesManagerBaseError):
    """ Raised when method fail to find logical population item. """


class LogicalSubPopulationError(MongoDBQueriesManagerBaseError):
    """ Raised when method fail to find logical sub population item. """


class MongoDBQueriesManager:
    """ MongoDBQueriesManager class.

    This class contain all method to convert string query to MongoDB query.

    Attributes:
        mongodb_operator (Dict[str, str]): MongoDB operator, used to convert query operators into MongoDB operators
        regex_dict (Dict[Union[str, re.Pattern], Any]): Contain all typing for cast into right format
    """

    mongodb_operator: Dict[str, str] = {
        '=': '$eq',
        '!=': '$ne',
        '>': '$gt',
        '>=': '$gte',
        '<': '$lt',
        '<=': '$lte',
        '!': '$exists',
        '': '$exists'
    }

    regex_dict: Dict[Union[str, re.Pattern], Any] = {
        re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'): float,
        re.compile(r'^[-+]?\d+$'): int,
        re.compile(r'^[12]\d{3}(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)(T|'
                   r' )?(([01][0-9]|2[0-3]):[0-5]\d(:[0-5]\d(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?)?$'):
            lambda date: parse(date, languages=['fr', 'en']),
        re.compile(r'^\w+(?=(,?,))(?:\1\w+)+$'): lambda list_value: list_value.split(','),
        re.compile(r'\/((?![*+?])(?:[^\r\n\[/\\]|\\.|\[(?:[^\r\n\]\\]|\\.)*\])+)'
                   r'\/((?:g(?:im?|mi?)?|i(?:gm?|mg?)?|m(?:gi?|ig?)?)?)'): re.compile,
        "true": lambda boolean: True,
        "false": lambda boolean: False,
        "null": lambda null: None,
        "none": lambda none: None,
    }

    custom_cast_dict: Optional[Dict[str, Callable]]

    def __init__(self, casters: Optional[Dict[str, Callable]] = None) -> None:
        self.custom_cast_dict = casters

    def filter_logic(self, filter_params: str) -> Dict[str, Any]:
        """ Build filter.

        Args:
            filter_params (str): Filter params from url query (ie, 'name=John')

        Returns:
            Dict[str, Any]: Dictionary with MongoDB filter
        """
        operator = self.find_operator(filter_params=filter_params)

        if operator != '':
            try:
                key, value = filter_params.split(operator)
            except ValueError as err:
                raise FilterError(f'Fail to split filter {filter_params} with operator {operator}') from err
        else:
            key, value = '', filter_params

        value = self.cast_value_logic(value)

        # $eq logic
        if not isinstance(value, list) and operator == '=':
            return {key: value}

        # $in, $nin, $exists logic
        if isinstance(value, list):
            # Cast list items
            casted_list_item = list()
            for item in value:
                casted_list_item.append(self.cast_value_logic(item))

            if operator == '=':
                return {key: {"$in": casted_list_item}}
            if operator == '!=':
                return {key: {"$nin": casted_list_item}}
            raise ListOperatorError('List operator not found')

        # $exists logic
        if operator in ['', '!']:
            return {value: {self.mongodb_operator[operator]: bool(operator == '')}}

        # $gt, $gte, $lt, $lte, $ne, logic
        return {key: {self.mongodb_operator[operator]: value}}

    def cast_value_logic(self, value: str) -> Any:
        """ Cast value into right type.

        Args:
            value (str): Value to cast

        Returns:
            Any: Casted value
        """
        if self.custom_cast_dict is not None:
            for rule, func in self.custom_cast_dict.items():
                if value.startswith(f'{rule}(') and value.endswith(')'):
                    try:
                        casted_value = func(value.replace(f'{rule}(', '')[:-1])
                    except Exception as err:
                        raise CustomCasterFail(f'Fail to cast {value} with caster {rule}') from err

                    return casted_value

        for regex, cast in self.regex_dict.items():
            if isinstance(regex, re.Pattern):
                if regex.match(value):
                    return cast(value)
            else:
                if regex == value.lower():
                    return cast(value)
        return value

    @staticmethod
    def find_operator(filter_params: str) -> str:
        """Return the right operator.

        Args:
            filter_params (str): Filter params (ie, 'name=John')

        Returns:
            str: Return operator
        """
        for operator in ['<=', '>=', '!=', '=', '>', '<', '!']:
            if filter_params.find(operator) > -1:
                return operator
        return ''

    @staticmethod
    def sort_logic(sort_params: str) -> Optional[List[Tuple]]:
        """ Convert sort query into MongoDB format.

        Notes:
            Work if `sort=` into url query.

        Args:
            sort_params (str): Sort param from url query (ie, 'sort=-created_at')

        Returns:
            Optional[List[Tuple]]: Optional tuple with MongoDB sort values
        """
        sort_params_final: List[Tuple] = list()
        value = sort_params.split('=')[1]

        if value:
            for param in value.split(','):
                if param.startswith('+'):
                    sort_params_final.append((param[1:], ASCENDING))
                elif param.startswith('-'):
                    sort_params_final.append((param[1:], DESCENDING))
                else:
                    sort_params_final.append((param, ASCENDING))
            return sort_params_final
        return None

    @staticmethod
    def text_operator_logic(text_param: str) -> str:
        """ Convert text query into MongoDB format.

        Args:
            text_param (str): Text param from url query (ie, '$text=java shop -coffee')

        Returns:
            int: Limit integer value
        """
        if text_param == "$text=":
            raise TextOperatorError('Bad $text value')

        return text_param.split('=')[1]

    @staticmethod
    def limit_logic(limit_param: str) -> int:
        """ Convert limit query into MongoDB format.

        Args:
            limit_param (str): Limit param from url query (ie, 'limit=5')

        Returns:
            int: Limit integer value
        """
        if limit_param == 'limit=':
            return 0

        try:
            limit_value = int(limit_param.split('=')[1])
        except ValueError as err:
            raise LimitError('Bad limit value') from err

        if limit_value < 0:
            raise LimitError('Negative limit value')

        return limit_value

    @staticmethod
    def skip_logic(skip_param: str) -> int:
        """ Convert skip query into MongoDB format.

        Args:
            skip_param (str): Skip param from url query (ie, 'limit=5')

        Returns:
            int: Skip integer value
        """
        if skip_param == 'skip=':
            return 0

        try:
            skip_value = int(skip_param.split('=')[1])
        except ValueError as err:
            raise SkipError('Bad skip value') from err

        if skip_value < 0:
            raise SkipError('Negative skip value')

        return skip_value

    @classmethod
    def _iter_on_population(cls, population: List[Dict[str, Any]], field: str, sign: int) -> bool:
        """ Used to add projection into population dict.

        Args:
            population (List[Dict[str, Any]]): List of asked population
            field (str): Field value in string format
            sign (int): The sign on the projection (0 for - / 1 for + or nothing)

        Returns:
            bool: Return true if the field as been added into a population otherwise false
        """
        pop_field = field.split('.', 1)
        for current_population in population:
            if current_population['path'] == pop_field[0]:
                if pop_field[1].find('.') >= 0:
                    cls._iter_on_population(population=current_population['population'], field=pop_field[1], sign=sign)
                else:
                    if not current_population.get('projection'):
                        current_population['projection'] = {}
                    current_population['projection'][pop_field[1]] = sign
                return True
        return False

    @classmethod
    def projection_logic(cls, projection_param: str,
                         population: Optional[List[Dict[str, Any]]]) -> Optional[Dict[str, Any]]:
        """ Convert projection query into MongoDB format.

        Notes:
            Work if `projection=` into url query.

        Args:
            projection_param (str): Projection param from url query (ie, 'fields=id,url')
            population (Optional[List[Dict[str, Any]]]): Optional population query values

        Returns:
            Optional[Dict[str, Any]]: Optional dictionary with MongoDB projection values
        """
        projection_params_final: Dict[str, Any] = dict()
        value = projection_param.split('=')[1]

        if value == '':
            return None

        for param in value.split(','):
            if population and param.find('.') > 0:
                if cls._iter_on_population(population=population, field=param[1:] if param.startswith('-') else param,
                                           sign=0 if param.startswith('-') else 1):
                    continue

            if param.startswith('-'):
                projection_params_final[param[1:]] = 0
            elif param.startswith('{') and param.endswith('}'):
                try:
                    json_value = json.loads(param)
                    projection_params_final[next(iter(json_value))] = json_value[next(iter(json_value))]
                except Exception as err:
                    raise ProjectionError('Fail to decode projection') from err
            else:
                projection_params_final[param] = 1
        return projection_params_final if projection_params_final != {} else None

    @classmethod
    def format_populate_value(cls, mongodb_query: Dict[str, Any], population_value: str) -> None:
        """ Convert population query into dict format.

        Args:
            mongodb_query (Dict[str, Any]): The actual mongodb query
            population_value (str): Population string value

        Returns:
            None: No return.
        """
        if population_value.find('.') >= 0:
            cls._iter_on_populate_value(mongodb_query, population_value)
        else:
            mongodb_query['population'].append({'path': population_value, 'projection': None})

    @classmethod
    def _iter_on_populate_value(cls, mongodb_query: Dict[str, Any], population_value: str) -> None:
        """ Used into format_populate_value method (split to respect the pylint config)

        Args:
            mongodb_query (Dict[str, Any]): The actual mongodb query
            population_value (str): Population string value

        Returns:
            None: No return.
        """
        path, sub_path = population_value.split('.', 1)
        if 'population' in mongodb_query:
            for population in mongodb_query['population']:
                if path == population['path']:
                    if 'population' not in population:
                        population['population'] = []

                    if sub_path.find('.') >= 0:
                        cls._iter_on_sub_populate_value(population=population, sub_path=sub_path)
                    else:
                        population['population'].append({'path': sub_path, 'projection': None})
                    break
            else:
                raise LogicalPopulationError('Fail to find logical population item')
        else:
            raise LogicalPopulationError('Fail to find logical population item')

    @classmethod
    def _iter_on_sub_populate_value(cls, population: Dict[str, Any], sub_path: str) -> None:
        """ Used into _iter_on_populate_value method (split to respect the pylint config)

        Args:
            population (Dict[str, Any]): The actual population
            sub_path (str): Sub path value

        Returns:
            None: No return.
        """
        path, sub_path = sub_path.split('.', 1)
        for sub_population in population['population']:
            if path == sub_population['path']:
                if sub_path.find('.') >= 0:
                    cls.format_populate_value(mongodb_query=sub_population,
                                              population_value=sub_path)
                else:
                    if 'population' not in sub_population:
                        sub_population['population'] = []
                    sub_population['population'].append({'path': sub_path, 'projection': None})
                break
        else:
            raise LogicalSubPopulationError('Fail to find logical sub population item')
