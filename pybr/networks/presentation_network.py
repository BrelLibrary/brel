import lxml.etree
# from pybr.networks import NetworkNode
# from pybr import PyBRComponent, qname
# from pybr.reportelements import PyBRAbstract, PyBRHypercube, PyBRMember, PyBRDimension, PyBRLineItems, i_report_element
from ..qname import QName

from .network_node import NetworkNode
from ..reportelements.pybr_abstract import PyBRAbstract
from ..reportelements.pybr_hypercube import PyBRHypercube
from ..reportelements.pybr_member import PyBRMember
from ..reportelements.pybr_dimension import PyBRDimension
from ..reportelements.pybr_lineitems import PyBRLineItems
from ..reportelements.i_report_element import IReportElement
from typing import cast

class PresentationNetwork:
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a PyBRComponent.
    """
    # TODO: write docstrings
    def __init__(self, root: NetworkNode | None, link_role: str, link_name: QName) -> None:
        self.__root = root
        self.__link_role = link_role
        self.__link_name = link_name
    
    # First class citizens
    def get_root(self) -> NetworkNode | None:
        """
        Get the root node of the presentation network
        @return: NetworkNode representing the root node of the network. Returns None if the network is empty.
        """
        return self.__root

    def get_link_role(self) -> str:
        """
        Get the link role of the presentation network
        @return: str containing the link role of the network. 
        Note: This returns the same as get_URL() on the PyBRComponent
        """
        return self.__link_role

    def get_link_name(self) -> QName:
        return self.__link_name

    # Second class citizens
    def get_all_nodes(self) -> list[NetworkNode]:
        """
        Get all nodes in the network
        @return: list[NetworkNode] containing all nodes in the network
        """

        # create a set to store all nodes in
        nodes = set()

        # recursive function to add all children of a node to the nodes set
        def add_children(node: NetworkNode) -> None:
            nodes.add(node)
            for child in node.get_children():
                add_children(child)
        
        # add all children of the root node to the nodes set
        if self.__root is not None:
            add_children(self.__root)

        # return the nodes set as a list
        return list(nodes)

    # Internal methods
    @staticmethod
    def __get_qname_from_href(href: str) -> QName:
        """
        Get a QName from an href attribute
        @param href: str containing the href attribute
        @param nsmap: dict[str, str] containing the namespace map
        @return: QName
        """
        # TODO: this feels like a hack
        # generate the qname from the href
        # Step 1. take the stuff after the #
        # Step 2. replace the _ with :
        # Step 3. parse the string as a QName
        href = href.split("#")[1]
        href = href.replace("_", ":")
        report_element_qname = QName.from_string(href)
        return report_element_qname

    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, report_elements: dict[QName, IReportElement]) -> tuple['PresentationNetwork', dict[QName, IReportElement]]:
        """
        Create a PresentationNetwork from an lxml.etree._Element. Note that this method also returns a dict containing all report elements.
        This is because the presentation network may change the internal representation of the report elements. More specifically, it may promote
        abstracts to line items.
        @param xml_element: lxml.etree._Element to be parsed. This element must be a link:presentationLink element.
        @param component: PyBRComponent to which the network belongs.
        @return: PresentationNetwork containing the presentation network and a dict containing all report elements
        """

        nsmap = QName.get_nsmap()

        # the node map is a map from the xlink:to attribute to the NetworkNode
        # it is used to link the NetworkNodes together as a tree
        nodes_map : dict[str, NetworkNode] = {}
        edges: list[tuple[str, str]] = []

        # get the xlink:role attribute
        link_role = xml_element.get(f"{{{nsmap['xlink']}}}role", None)

        # define the link:presentationLink as a QName
        link_name = QName.from_string(xml_element.tag)

        # first get all link:presentationArc elements
        xml_arcs = xml_element.findall(f".//link:presentationArc", namespaces=nsmap)
        for xml_arc in xml_arcs:
            # find the xlink:to and to attributes
            xml_to = xml_arc.get(f"{{{nsmap['xlink']}}}to")
            
            # find the link:loc xml element, where the xlink:label attribute is the xlink:to attribute
            loc_xml = xml_element.find(f".//link:loc[@{{{nsmap['xlink']}}}label='{xml_to}']", namespaces=nsmap)

            # get the xlink:href attribute of the loc element
            href = loc_xml.get(f"{{{nsmap['xlink']}}}href")

            # get the QName from the href
            report_element_qname = cls.__get_qname_from_href(href)

            report_element = report_elements[report_element_qname]

            # create the NetworkNode
            node = NetworkNode.from_xml(xml_arc, report_element)

            # get the xlink:from attribute from the arc element
            xml_from = xml_arc.get(f"{{{nsmap['xlink']}}}from")

            # add the node to the node map
            nodes_map[xml_to] = node

            # add the edge to the edges list
            edges.append((xml_from, xml_to))
        

        # second pass over all nodes to link them together. Also find the root node
        root = None
        for from_node_name, to_node_name in edges:
            to_node = nodes_map[to_node_name]
            if from_node_name not in nodes_map and root is None:
                # there is exactly one node that is not in the nodes map. This is the root node
                # first, get the locator element
                loc_xml = xml_element.find(f".//link:loc[@{{{nsmap['xlink']}}}label='{from_node_name}']", namespaces=nsmap)

                # then get the xlink:href attribute
                href = loc_xml.get(f"{{{nsmap['xlink']}}}href")

                # then get the QName from the href
                report_element_qname = cls.__get_qname_from_href(href)

                # then create the root networknode
                root = NetworkNode(
                    report_elements[report_element_qname], 
                    [], 
                    to_node.get_arc_role(), 
                    link_name, 
                    to_node.get_preferred_label_role()
                )
                nodes_map[from_node_name] = root
            
            from_node = nodes_map[from_node_name]
            from_node.add_child(to_node)
        
        # third pass
        # walk through the tree and change all suitable abstracts to line items
        # there are two criteria for an abstract to be changed to a line item:
        # 1. Hypercube dimension rule: if its parent is a hypercube, then it is a line item
        # 2. Implicit hypercube rule: if if it is the root node and it does not have hypercube children, then it is a line item
        report_elements_to_change: list[str] = []
        for node_name, node in nodes_map.items():
            if isinstance(node.get_report_element(), PyBRAbstract):
                parent = next(filter(
                    lambda x: node in x.get_children(),
                    nodes_map.values()
                ), None)


                if parent is not None and isinstance(parent.get_report_element(), PyBRHypercube):
                    report_elements_to_change.append(node_name)
                
                if parent is None and not any(map(lambda x: isinstance(x.get_report_element(), PyBRHypercube), node.get_children())):
                    report_elements_to_change.append(node_name)
        
        print(report_elements_to_change)
        for report_element_to_change in report_elements_to_change:

            # create a lineitem from the abstract
            abstract = cast(PyBRAbstract, nodes_map[report_element_to_change].get_report_element())

            assert isinstance(abstract, PyBRAbstract)

            line_item = PyBRLineItems(abstract.get_name(), abstract.get_labels())

            # update the report element dict
            report_elements[abstract.get_name()] = line_item

            # update the node
            nodes_map[report_element_to_change]._set_report_element(line_item)
        
        if root is None and len(nodes_map) > 0:
            raise Exception(f"Could not find root node of non-empty presentation network {link_role}")
        
        # create the presentation network
        return cls(root, link_role, link_name), report_elements
    