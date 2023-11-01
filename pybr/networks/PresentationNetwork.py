import lxml.etree
from pybr.networks import NetworkNode
from pybr import PyBRComponent, QName
from pybr.reportelements import IReportElement

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
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, report_elements: dict[QName, IReportElement]) -> 'PresentationNetwork':
        """
        Create a PresentationNetwork from an lxml.etree._Element.
        @param xml_element: lxml.etree._Element to be parsed. This element must be a link:presentationLink element.
        @param component: PyBRComponent to which the network belongs.
        @return: PresentationNetwork
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

            # TODO: this feels like a hack
            # generate the qname from the href
            # Step 1. take the stuff after the #
            # Step 2. replace the _ with :
            # Step 3. parse the string as a QName
            href = href.split("#")[1]
            href = href.replace("_", ":")
            report_element_qname = QName.from_string(href)
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
        for from_node, to_node in edges:
            if from_node not in nodes_map:
                root = nodes_map[to_node]
            else:
                nodes_map[from_node].add_child(nodes_map[to_node])
        
        if root is None and len(nodes_map) > 0:
            raise Exception(f"Could not find root node of non-empty presentation network {link_role}")
        
        # create the presentation network
        return cls(root, link_role, link_name)

