import lxml.etree

# from pybr.reportelements import i_report_element
# from pybr import PyBRLabelRole, QName
from ..reportelements.i_report_element import IReportElement
from ..pybr_label import PyBRLabelRole
from ..qname import QName

class NetworkNode():
    """
    Class for representing a node in a network.
    Since a node can have children, nodes can also be viewed as trees.
    """
    # TODO: docstrings

    def __init__(
            self, 
            report_element: IReportElement, 
            children: list['NetworkNode'],
            arc_role: str,
            arc_name: QName,
            preferred_label_role: PyBRLabelRole = PyBRLabelRole.STANDARD_LABEL,
            order: int = 0
            ):
        self.__report_element = report_element
        self.__children = children
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__preferred_label_role = preferred_label_role
        self.__order = order
    
    # First class citizens
    def get_report_element(self) -> IReportElement:
        """
        Returns the report element associated with this node
        @return: IReportElement associated with this node
        """
        return self.__report_element
    
    def get_children(self) -> list['NetworkNode']:
        """
        Returns the children of this node
        @return: list[NetworkNode] containing the children of this node
        """
        return self.__children

    def get_preferred_label_role(self) -> PyBRLabelRole:
        """
        Returns the preferred label role of this node
        @return: str containing the preferred label role of this node
        """
        return self.__preferred_label_role

    def get_order(self) -> int:
        """
        Returns the order of this node
        @return: int containing the order of this node
        """
        return self.__order

    # Second class citizens
    def get_all_decendents(self) -> list['NetworkNode']:
        raise NotImplementedError
    
    def get_arc_role(self) -> str:
        return self.__arc_role
    
    def get_arc_name(self) -> QName:
        return self.__arc_name
    
    def __str__(self) -> str:
        """
        Returns a string representation of this node
        @return: str containing a string representation of this node
        """

        return f"NetworkNode(report_element={self.__report_element}, no. children={len(self.__children)}"
    
    # Internal methods
    def add_child(self, child: 'NetworkNode'):
        """
        Add a child to this node
        @param child: NetworkNode to be added as a child
        """
        self.__children.append(child)
    
    def _set_report_element(self, report_element: IReportElement):
        """
        Set the report element of this node
        @param report_element: IReportElement to be set as the report element
        """
        self.__report_element = report_element

    @classmethod
    def from_xml(cls, xml_arc: lxml.etree._Element, report_element: IReportElement) -> 'NetworkNode':
        """
        Create a NetworkNode from an lxml.etree._Element.
        """

        nsmap = QName.get_nsmap()
        
        # get the preferred label role
        preferred_label_role = PyBRLabelRole.from_url(xml_arc.attrib.get("preferredLabel"))

        # get the arc role
        # TODO: ask ghislain if I should create an arcrole enum instead of a str
        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")

        # get the order and parse it to an int
        order = int(xml_arc.attrib.get("order"))

        # the arcname is "link:presentationLink" as a QName for all presentation networks
        # TODO: make this work for calculation networks and definition networks as well
        arc_name = QName.from_string("link:presentationLink")

        # create the node
        return cls(report_element, [], arc_role, arc_name, preferred_label_role, order)




