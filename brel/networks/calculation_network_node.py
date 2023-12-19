import lxml.etree

from brel.networks import INetworkNode
from brel.reportelements import IReportElement, Concept
from brel import BrelLabelRole, QName

from typing import cast

from brel.resource import IResource

class CalculationNetworkNode(INetworkNode):
    """
    Class for representing a node in a network.
    Since a node can have children, nodes can also be viewed as trees.
    """

    def __init__(
            self, 
            report_element: IReportElement, 
            children: list['CalculationNetworkNode'],
            arc_role: str,
            arc_name: QName,
            link_role: str,
            link_name: QName,
            weight: float = 1.0,
            order: int = 1
            ):
        if not isinstance(report_element, Concept):
            raise TypeError(f"report_element must be of type Concept, but is of type {type(report_element)}")

        self.__report_element = report_element
        self.__children = children
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__order = order
        self.__weight = weight
    
    # First class citizens
    def get_report_element(self) -> IReportElement:
        """
        Returns the report element associated with this node
        @return: IReportElement associated with this node
        """
        return self.__report_element
    
    def get_resource(self) -> IResource:
        """
        Would return the resource associated with this node, but calculation network nodes do not point to resources
        @raises ValueError: CalculationNetworkNode does not point to a resource
        """
        raise ValueError("CalculationNetworkNode does not point to a resource")
    
    def is_a(self) -> str:
        """
        @return: str containing 'report element'
        """
        return 'report element'
    
    def get_children(self) -> list['INetworkNode']:
        """
        Returns the children of this node
        @return: list[NetworkNode] containing the children of this node
        """
        # return lsitself.__children

        return list(map(lambda x: cast(INetworkNode, x), self.__children))

    def get_weight(self) -> float:
        """
        Returns the weight of this node
        @return: float containing the weight of this node
        """
        return self.__weight
    
    def get_order(self) -> int:
        """
        Returns the order of this node
        @return: int containing the order of this node
        """
        return self.__order
    
    def get_arc_role(self) -> str:
        return self.__arc_role
    
    def get_arc_name(self) -> QName:
        return self.__arc_name
    
    def get_link_role(self) -> str:
        return self.__link_role
    
    def get_link_name(self) -> QName:
        return self.__link_name
    
    def __str__(self) -> str:
        """
        Returns a string representation of this node
        @return: str containing a string representation of this node
        """

        return f"NetworkNode(report_element={self.__report_element}, no. children={len(self.__children)}"
    
    # Internal methods
    def add_child(self, child: INetworkNode):
        """
        Add a child to this node
        @param child: NetworkNode to be added as a child
        """
        if not isinstance(child, CalculationNetworkNode):
            raise TypeError("child must be of type CalculationNetworkNode")

        self.__children.append(child)
        self.__children.sort(key=lambda node: node.get_order())

        # sanity check to make sure the weights of the children are legal. The following configurations are illegal:
        # - self = debit, child = debit, child_weight < 0
        # - self = debit, child = credit, child_weight > 0
        # - self = credit, child = debit, child_weight > 0
        # - self = credit, child = credit, child_weight < 0

        self_balance = self.__report_element.get_balance_type()
        child_balance = cast(Concept, child.get_report_element()).get_balance_type()
        child_weight = child.get_weight()
        if (self_balance == "debit" and child_balance == "debit" and child_weight < 0):
            raise ValueError(f"the child {child} has a negative weight, but the parent {self} has a debit balance")
        elif (self_balance == "debit" and child_balance == "credit" and child_weight > 0):
            raise ValueError(f"the child {child} has a positive weight, but the parent {self} has a debit balance")
        elif (self_balance == "credit" and child_balance == "debit" and child_weight > 0):
            raise ValueError(f"the child {child} has a positive weight, but the parent {self} has a credit balance")
        elif (self_balance == "credit" and child_balance == "credit" and child_weight < 0):
            raise ValueError(f"the child {child} has a negative weight, but the parent {self} has a credit balance")
