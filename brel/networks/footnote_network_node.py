from brel.resource import IResource, BreelFootnote
from brel.networks import INetworkNode
from brel.reportelements import IReportElement
from brel import QName

from typing import cast

class FootnoteNetworkNode(INetworkNode):
    """
    Class for representing a footnote network node in a footnote network.
    Since a node can have children, nodes can also be viewed as trees.
    """
    def __init__(
            self,
            points_to: BreelFootnote | IReportElement,
            children: list['FootnoteNetworkNode'],
            arc_role: str,
            arc_name: QName,
            link_role: str,
            link_name: QName,
            order: float = 1.0
                  ) -> None:

        self.__points_to = points_to
        self.__children = children
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__order = order

    # First class citizens
    def get_report_element(self) -> IReportElement:
        if not isinstance(self.__points_to, IReportElement):
            raise ValueError(f"The FootnoteNetworkNode points to a resource. Use get_resource() instead")
        return self.__points_to
    
    def get_resource(self) -> IResource:
        if not isinstance(self.__points_to, IResource):
            raise ValueError(f"The FootnoteNetworkNode points to a report element. Use get_report_element() instead")
        return self.__points_to
    
    def is_a(self) -> str:
        if isinstance(self.__points_to, IReportElement):
            return 'report element'
        elif isinstance(self.__points_to, IResource):
            return 'resource'
        else:
            raise ValueError(f"The FootnoteNetworkNode with label {self.__points_to.get_label()} does not point to report elements or resources. It points to {self.__points_to}. Use get_report_element() or get_resource() instead")
    
    def get_children(self) -> list[INetworkNode]:
        return cast(list[INetworkNode], self.__children)
    
    def get_order(self) -> float:
        return self.__order
    
    def get_arc_role(self) -> str:
        return self.__arc_role
    
    def get_arc_name(self) -> QName:
        return self.__arc_name
    
    def get_link_role(self) -> str:
        return self.__link_role
    
    def get_link_name(self) -> QName:
        return self.__link_name
    
    # Internal methods
    def add_child(self, child: INetworkNode):
        """
        Add a child to the node.
        @param child: the child to add
        """
        if not isinstance(child, FootnoteNetworkNode):
            raise ValueError(f"The child {child} is not a FootnoteNetworkNode")
        self.__children.append(child)
        self.__children.sort(key=lambda x: x.get_order())

    def _set_report_element(self, report_element: IReportElement):
        """
        Set the report element of this node
        @param report_element: IReportElement to be set as the report element
        """
        self.__points_to = report_element
