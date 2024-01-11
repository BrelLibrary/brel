import lxml
import lxml.etree
from abc import ABC, abstractmethod
from brel import QName, QNameNSMap, Fact
from brel.reportelements import IReportElement
from brel.resource import IResource
from brel.networks import INetwork, INetworkNode


class IXMLNetworkFactory(ABC):
    def __init__(self, qname_nsmap: QNameNSMap) -> None:
        self.__qname_nsmap = qname_nsmap

    def get_qname_nsmap(self) -> QNameNSMap:
        return self.__qname_nsmap

    @abstractmethod
    def create_network(
        self, xml_link: lxml.etree._Element, roots: list[INetworkNode]
    ) -> INetwork:
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
    def update_report_elements(
        self, report_elements: dict[QName, IReportElement], network: INetwork
    ) -> dict[QName, IReportElement]:
        raise NotImplementedError

    @abstractmethod
    def is_physical(self) -> bool:
        raise NotImplementedError
