"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 10 April 2025

====================
"""

from typing import Any, Dict, Callable
from brel.data.aspect.aspect_repository import AspectRepository
from brel.data.factory import (
    create_aspect_repository,
    create_report_element_repository,
    create_error_repository,
    create_component_repository,
    create_network_repository,
    create_fact_repository,
    create_characteristic_repository,
)
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.data.errors.error_repository import ErrorRepository
from brel.data.fact.fact_repository import FactRepository
from brel.data.characteristic.characteristic_repository import CharacteristicRepository
from brel.data.network.network_repository import NetworkRepository
from brel.data.component.component_repository import ComponentRepository
from brel.qname import QNameNSMap


class FilingContext:
    def __init__(self) -> None:
        self.__cache: Dict[str, Any] = {}

    def __lazy_cache[T](self, key: str, factory_function: Callable[[], T]) -> T:
        if key not in self.__cache:
            self.__cache[key] = factory_function()
        return self.__cache[key]

    def get_report_element_repository(self) -> ReportElementRepository:
        return self.__lazy_cache(
            "report_element_repository", lambda: create_report_element_repository()
        )

    def get_error_repository(self) -> ErrorRepository:
        return self.__lazy_cache("error_repository", lambda: create_error_repository())

    def get_fact_repository(self) -> FactRepository:
        return self.__lazy_cache("fact_repository", lambda: create_fact_repository())

    def get_characteristic_repository(self) -> CharacteristicRepository:
        return self.__lazy_cache(
            "characteristic_repository", lambda: create_characteristic_repository()
        )

    def get_network_repository(self) -> NetworkRepository:
        return self.__lazy_cache(
            "network_repository", lambda: create_network_repository()
        )

    def get_component_repository(self) -> ComponentRepository:
        return self.__lazy_cache(
            "component_repository", lambda: create_component_repository()
        )

    def get_aspect_repository(self) -> AspectRepository:
        return self.__lazy_cache(
            "aspect_repository", lambda: create_aspect_repository()
        )

    def get_nsmap(self) -> QNameNSMap:
        # TODO schmidi: rework NSMap
        return self.__lazy_cache("nsmap", lambda: QNameNSMap())
