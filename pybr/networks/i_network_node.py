from abc import ABC, abstractmethod
from pybr.reportelements import IReportElement
from pybr import QName

class INetworkNode(ABC):
    """
    Class for representing a node in a network.
    Since a node can have children, nodes can also be viewed as trees.
    """
    
    # First class citizens
    @abstractmethod
    def get_report_element(self) -> IReportElement:
        """
        Returns the report element associated with this node
        @return: IReportElement associated with this node
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_children(self) -> list['INetworkNode']:
        """
        Returns the children of this node
        @return: list[NetworkNode] containing the children of this node
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_arc_role(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_arc_name(self) -> QName:
        raise NotImplementedError


    # Second class citizens
    def get_all_descendents(self) -> list['INetworkNode']:
        """
        Returns a list containing all decendents of this node
        @return: list[NetworkNode] containing all decendents of this node
        """
        decentents = set()
        worklist = [self]
        while len(worklist) > 0:
            node = worklist.pop()
            decentents.add(node)
            worklist.extend(node.get_children())
        
        return list(decentents)
    
    def __str__(self) -> str:
        """
        Returns a string representation of this node
        @return: str containing a string representation of this node
        """

        return f"NetworkNode(report_element={self.get_report_element()}, no. children={len(self.get_children())}"
    
    # Internal methods
    def add_child(self, child: 'INetworkNode'):
        """
        Add a child to this node
        @param child: NetworkNode to be added as a child
        """
        raise NotImplementedError
    


