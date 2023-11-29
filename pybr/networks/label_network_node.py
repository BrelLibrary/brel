from pybr.networks import INetworkNode
from pybr.reportelements import IReportElement
from pybr import QName

from typing import cast

DEBUG = False

class LabelNetworkNode(INetworkNode):
    """
    Class for representing a label network node in a label network.
    Label networks are essentially sets of individual report elements.
    """
    def  __init__(
            self,
            report_element: IReportElement,
            arc_role: str,
            arc_name: QName,
                  ) -> None:
        self.__report_element = report_element
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__children: list[INetworkNode] = []
    
    # First class citizens
    def get_report_element(self) -> IReportElement:
        return self.__report_element
    
    def get_children(self) -> list[INetworkNode]:
        return self.__children
    
    def get_order(self) -> int:
        return 1
    
    def get_arc_role(self) -> str:
        return self.__arc_role
    
    def get_arc_name(self) -> QName:
        return self.__arc_name
    
    # Internal methods
    def add_child(self, child: INetworkNode):
        if DEBUG:  # pragma: no cover
            print("Warning: LabelNetworkNodes should not have children")
        
    
    def _set_report_element(self, report_element: IReportElement):
        """
        Set the report element of this node
        @param report_element: IReportElement to be set as the report element
        """
        self.__report_element = report_element
        