"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 123May 2025

====================
"""

import os
from brel.data.aspect.aspect_repository import AspectRepository
from brel.data.aspect.in_memory_aspect_repository import InMemoryAspectRepository
from brel.data.file.file_repository import FileRepository
from brel.data.file.pyfs_file_repository import PyFsFileRepository
from brel.data.namespace.in_memory_namespace_repository import (
    InMemoryNamespaceRepository,
)
from brel.data.namespace.namespace_repository import NamespaceRepository
from brel.data.report_element.in_memory_report_element_repository import (
    InMemoryReportElementRepository,
)
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.data.errors.in_memory_error_repository import InMemoryErrorRepository
from brel.data.errors.error_repository import ErrorRepository
from brel.data.fact.fact_repository import FactRepository
from brel.data.fact.in_memory_fact_repository import InMemoryFactRepository
from brel.data.characteristic.in_memory_characteristic_repository import (
    InMemoryCharacteristicRepository,
)
from brel.data.characteristic.characteristic_repository import CharacteristicRepository
from brel.data.network.network_repository import NetworkRepository
from brel.data.network.in_memory_network_repository import InMemoryNetworkRepository
from brel.data.component.component_repository import ComponentRepository
from brel.data.component.in_memory_component_repository import (
    InMemoryComponentRepository,
)
from brel.data.xml.xml_repository import XMLRepository


def create_report_element_repository() -> ReportElementRepository:
    return InMemoryReportElementRepository()


def create_error_repository() -> ErrorRepository:
    return InMemoryErrorRepository()


def create_component_repository() -> ComponentRepository:
    return InMemoryComponentRepository()


def create_characteristic_repository() -> CharacteristicRepository:
    return InMemoryCharacteristicRepository()


def create_network_repository() -> NetworkRepository:
    return InMemoryNetworkRepository()


def create_fact_repository() -> FactRepository:
    return InMemoryFactRepository()


def create_aspect_repository() -> AspectRepository:
    return InMemoryAspectRepository()


def create_namespace_repository() -> NamespaceRepository:
    return InMemoryNamespaceRepository()


def create_file_repository() -> FileRepository:
    cache_location = os.path.join(os.path.expanduser("~"), ".brel", "dts_cache")
    return PyFsFileRepository(cache_location, clear_cache=False)


def create_xml_repository() -> XMLRepository:
    return XMLRepository()
