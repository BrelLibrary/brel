from abc import ABC, abstractmethod

import lxml
import lxml.etree
from typing import Mapping, Iterable, Tuple

from brel import Fact, QName, QNameNSMap
from brel.networks import INetwork, INetworkNode
from brel.reportelements import IReportElement
from brel.resource import IResource


class IXMLNetworkFactory(ABC):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        self.__qname_nsmap = qname_nsmap

    def get_qname_nsmap(self) -> QNameNSMap:
        return self.__qname_nsmap

    @abstractmethod
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        raise NotImplementedError

    @abstractmethod
    def create_node(
        self,
        xml_link: lxml.etree._Element,
        xml_referenced_element: lxml.etree._Element,
        xml_arc: lxml.etree._Element | None,
        points_to: IReportElement | IResource | Fact,
    ) -> INetworkNode:
        raise NotImplementedError

    @abstractmethod
    def update_report_elements(self, report_elements: Mapping[QName, IReportElement], network: INetwork):
        raise NotImplementedError

    @abstractmethod
    def is_physical(self) -> bool:
        raise NotImplementedError

    # helper methods
    def _clark(self, prefix: str, local_name: str) -> str:
        """
        Given a prefix, a local name, and a prefix to URL mapping, return the clark notation.
        :param prefix: The prefix.
        :param local_name: The local name.
        :returns str: The clark notation.
        """
        url = self.__qname_nsmap.get_nsmap()[prefix]
        return f"{{{url}}}{local_name}"

    def _make_qname(self, qname_str: str) -> QName:
        """
        Given a string in clark notation, return a QName object.
        :param qname_str: The clark notation.
        :returns QName: The QName object.
        """
        return QName.from_string(qname_str, self.__qname_nsmap)
