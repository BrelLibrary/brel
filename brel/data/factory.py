from brel.data.aspect.aspect_repository import AspectRepository
from brel.data.aspect.in_memory_aspect_repository import InMemoryAspectRepository
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
