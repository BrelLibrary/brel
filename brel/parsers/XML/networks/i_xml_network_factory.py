"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

from abc import ABC, abstractmethod

from lxml.etree import _Element  # type: ignore

from brel.brel_fact import Fact
from brel.networks import INetwork, INetworkNode
from brel.reportelements import IReportElement
from brel.resource import IResource
from brel.data.report_element.report_element_repository import ReportElementRepository


class IXMLNetworkFactory(ABC):
    @abstractmethod
    def create_network(self, xml_link: _Element, roots: list[INetworkNode]) -> INetwork:
        raise NotImplementedError

    @abstractmethod
    def create_node(
        self,
        xml_link: _Element,
        xml_referenced_element: _Element,
        xml_arc: _Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        raise NotImplementedError

    def update_report_elements(
        self, report_element_repository: ReportElementRepository, network: INetwork
    ) -> None:
        pass

    @abstractmethod
    def is_physical(self) -> bool:
        raise NotImplementedError
