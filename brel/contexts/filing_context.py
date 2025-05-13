"""
====================

- author: Robin Schmidiger
- version: 0.3
- date: 8 May 2025

====================
"""

from typing import Any, Dict, Callable
from brel.data.aspect.aspect_repository import AspectRepository
from brel.data.factory import (
    create_aspect_repository,
    create_file_repository,
    create_namespace_repository,
    create_report_element_repository,
    create_error_repository,
    create_component_repository,
    create_network_repository,
    create_fact_repository,
    create_characteristic_repository,
    create_xml_repository,
)
from brel.data.file.file_repository import FileRepository
from brel.data.namespace.namespace_repository import NamespaceRepository
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.data.errors.error_repository import ErrorRepository
from brel.data.fact.fact_repository import FactRepository
from brel.data.characteristic.characteristic_repository import CharacteristicRepository
from brel.data.network.network_repository import NetworkRepository
from brel.data.component.component_repository import ComponentRepository
from brel.data.xml.xml_repository import XMLRepository
from brel.services.factory import (
    create_file_service,
    create_report_element_service,
    create_xml_service,
)
from brel.services.file.file_service import FileService
from brel.services.report_element.report_element_service import ReportElementService
from brel.services.xml.xml_service import XMLService


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

    def get_namespace_repository(self) -> NamespaceRepository:
        return self.__lazy_cache(
            "namespace_repository", lambda: create_namespace_repository()
        )

    def get_file_repository(self) -> FileRepository:
        return self.__lazy_cache("file_repository", lambda: create_file_repository())

    def get_file_service(self) -> FileService:
        return self.__lazy_cache(
            "file_service",
            lambda: create_file_service(self.get_file_repository()),
        )

    def get_xml_repository(self) -> XMLRepository:
        return self.__lazy_cache("xml_repository", lambda: create_xml_repository())

    def get_xml_service(self) -> XMLService:
        return self.__lazy_cache(
            "xml_service",
            lambda: create_xml_service(
                self.get_file_service(), self.get_xml_repository()
            ),
        )

    def get_report_element_service(self) -> ReportElementService:
        return self.__lazy_cache(
            "report_element_service",
            lambda: create_report_element_service(
                self.get_report_element_repository(), self.get_namespace_repository()
            ),
        )
