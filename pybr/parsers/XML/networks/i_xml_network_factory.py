import lxml
import lxml.etree
from abc import ABC, abstractmethod
from pybr import QName
from pybr.reportelements import IReportElement
from pybr.networks import INetwork, INetworkNode

class IXMLNetworkFactory(ABC):
    @abstractmethod
    def create_network(self, xml_link: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        raise NotImplementedError

    @abstractmethod
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        raise NotImplementedError

    @abstractmethod
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        raise NotImplementedError
    
    @abstractmethod
    def update_report_elements(self, report_elements: dict[QName, IReportElement], network: INetwork) -> dict[QName, IReportElement]:
        raise NotImplementedError