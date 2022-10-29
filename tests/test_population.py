#!/usr/bin/env python3
# Copyright (c) Modos Team, 2020

from __future__ import annotations

import pytest

from mongo_queries_manager import LogicalPopulationError, LogicalSubPopulationError, mqm


class TestPopulation:
    def test_empty_population(self) -> None:
        query_result = mqm(string_query="populate=", populate=True)

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [],
        }

    def test_simple_population(self) -> None:
        query_result = mqm(string_query="populate=user", populate=True)

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [{"path": "user", "projection": None}],
        }

    def test_multi_population(self) -> None:
        query_result = mqm(string_query="populate=user,settings", populate=True)

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {"path": "user", "projection": None},
                {"path": "settings", "projection": None},
            ],
        }

    def test_multi_population_2(self) -> None:
        query_result = mqm(string_query="populate=user,user.settings", populate=True)

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {
                    "path": "user",
                    "projection": None,
                    "population": [{"path": "settings", "projection": None}],
                }
            ],
        }

    def test_multi_population_3(self) -> None:
        query_result = mqm(
            string_query="populate=user,user.settings,user.comments,user.info",
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {
                    "path": "user",
                    "projection": None,
                    "population": [
                        {"path": "settings", "projection": None},
                        {"path": "comments", "projection": None},
                        {"path": "info", "projection": None},
                    ],
                }
            ],
        }

    def test_multi_population_4(self) -> None:
        query_result = mqm(
            string_query="populate=user,user.settings,user.settings.info,user.settings.info.rates",
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {
                    "path": "user",
                    "projection": None,
                    "population": [
                        {
                            "path": "settings",
                            "projection": None,
                            "population": [
                                {
                                    "path": "info",
                                    "projection": None,
                                    "population": [
                                        {"path": "rates", "projection": None}
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

    def test_multi_population_5(self) -> None:
        query_result = mqm(
            string_query="populate=user,user.settings,user.settings.notifications,user.settings.configuration",
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {
                    "path": "user",
                    "projection": None,
                    "population": [
                        {
                            "path": "settings",
                            "projection": None,
                            "population": [
                                {"path": "notifications", "projection": None},
                                {"path": "configuration", "projection": None},
                            ],
                        }
                    ],
                }
            ],
        }

    def test_multi_population_6(self) -> None:
        query_result = mqm(
            string_query="populate=user,user.life,user.life.info,user.settings,user.settings.notifications",
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {
                    "path": "user",
                    "projection": None,
                    "population": [
                        {
                            "path": "life",
                            "projection": None,
                            "population": [{"path": "info", "projection": None}],
                        },
                        {
                            "path": "settings",
                            "projection": None,
                            "population": [
                                {"path": "notifications", "projection": None}
                            ],
                        },
                    ],
                }
            ],
        }

    def test_simple_population_with_projection(self) -> None:
        query_result = mqm(
            string_query="fields=-created_at,-updated_at,hives.label&populate=hives",
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"created_at": 0, "updated_at": 0},
            "population": [{"path": "hives", "projection": {"label": 1}}],
        }

    def test_multi_population_with_multi_projection(self) -> None:
        query_result = mqm(
            string_query=(
                "fields=-created_at,-updated_at,hives.label,hives._id,"
                "data.temperature&populate=hives,data"
            ),
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"created_at": 0, "updated_at": 0},
            "population": [
                {"path": "hives", "projection": {"label": 1, "_id": 1}},
                {"path": "data", "projection": {"temperature": 1}},
            ],
        }

    def test_multi_population_with_multi_projection_2(self) -> None:
        query_result = mqm(
            string_query=(
                "fields=-created_at,-updated_at,-service.created_at,-service.updated_at,"
                "-service.description.created_at,-service."
                "description.updated_at&populate=service,service.description,service."
                "description.picture,animal,animal.info"
            ),
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"created_at": 0, "updated_at": 0},
            "population": [
                {
                    "path": "service",
                    "projection": {"created_at": 0, "updated_at": 0},
                    "population": [
                        {
                            "path": "description",
                            "projection": {"created_at": 0, "updated_at": 0},
                            "population": [{"path": "picture", "projection": None}],
                        }
                    ],
                },
                {
                    "path": "animal",
                    "projection": None,
                    "population": [{"path": "info", "projection": None}],
                },
            ],
        }

    def test_bad_population_logic(self) -> None:
        with pytest.raises(LogicalPopulationError) as excinfo:
            _ = mqm(string_query="populate=service.description", populate=True)

        assert excinfo.value.__str__() == "Fail to find logical population item"

    def test_bad_population_logic_2(self) -> None:
        with pytest.raises(LogicalPopulationError) as excinfo:
            _ = mqm(
                string_query=(
                    "populate=service,service.description,service.description.toto.titi"
                ),
                populate=True,
            )

        assert excinfo.value.__str__() == "Fail to find logical population item"

    def test_bad_sub_population_logic(self) -> None:
        with pytest.raises(LogicalSubPopulationError) as excinfo:
            _ = mqm(
                string_query=(
                    "populate=service,service.description,"
                    "service.description.info,service.descriptions.info"
                ),
                populate=True,
            )

        assert excinfo.value.__str__() == "Fail to find logical sub population item"

    def test_bad_sub_population_logic_2(self) -> None:
        with pytest.raises(LogicalSubPopulationError) as excinfo:
            _ = mqm(
                string_query=(
                    "populate=service,service.description,service.description.info,"
                    "service.description.info,service.description.info.toto,"
                    "service.descriptions.info.titi"
                ),
                populate=True,
            )

        assert excinfo.value.__str__() == "Fail to find logical sub population item"

    def test_sub_population_alex(self) -> None:
        query_result = mqm(
            string_query=(
                "populate=animal,crossbreed,crossbreed.crossbreeds,company,service,"
                "service.service_description,pet&fields=-company.settings.booking"
            ),
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {"path": "animal", "projection": None},
                {
                    "path": "crossbreed",
                    "projection": None,
                    "population": [{"path": "crossbreeds", "projection": None}],
                },
                {"path": "company", "projection": {"settings.booking": 0}},
                {
                    "path": "service",
                    "projection": None,
                    "population": [{"path": "service_description", "projection": None}],
                },
                {"path": "pet", "projection": None},
            ],
        }

    def test_sub_population_alex_2(self) -> None:
        query_result = mqm(
            string_query=(
                "populate=animal,crossbreed,crossbreed.crossbreeds,company,service,"
                "service.service_description,pet&fields=-company.settings.booking,"
                "-company.settings.toto"
            ),
            populate=True,
        )

        assert query_result == {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
            "population": [
                {"path": "animal", "projection": None},
                {
                    "path": "crossbreed",
                    "projection": None,
                    "population": [{"path": "crossbreeds", "projection": None}],
                },
                {
                    "path": "company",
                    "projection": {"settings.booking": 0, "settings.toto": 0},
                },
                {
                    "path": "service",
                    "projection": None,
                    "population": [{"path": "service_description", "projection": None}],
                },
                {"path": "pet", "projection": None},
            ],
        }
