import lxml
import lxml.etree
from typing import cast
from pybr import QName, BrelLabelRole
from pybr.reportelements import IReportElement, PyBRAbstract, PyBRHypercube, PyBRLineItems
from pybr.networks import INetwork, INetworkNode, PresentationNetwork, PresentationNetworkNode

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory

class PresentationNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        # TODO: make assertions
        nsmap = QName.get_nsmap()

        if len(roots) != 1:
            raise ValueError("roots must have exactly one element")
        if not isinstance(roots[0], PresentationNetworkNode):
            raise TypeError("roots must be of type PresentationNetworkNode")

        root = roots[0]
        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_name = QName.from_string(xml_link_element.tag)


        if link_role is None:
            raise ValueError("link_role must not be None")

        return PresentationNetwork(root, link_role, link_name)
    
    def create_internal_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        preferred_label = xml_arc.attrib.get("preferredLabel")
        if preferred_label is None:
            # The preferredLabel attribute is optional. If it is not present, the preferred label role is the standard label
            preferred_label_role = BrelLabelRole.STANDARD_LABEL
        if not isinstance(preferred_label, str):
            raise TypeError("preferred_label must be a string")
        
        preferred_label_role = BrelLabelRole.from_url(preferred_label)
        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = int(xml_arc.attrib.get("order") or 1)
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if not isinstance(arc_role, str):
            raise TypeError(f"arcrole attribute on arc element {xml_arc} is not a string")
        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(f"role attribute on link element {xml_link} is not a string")

        return PresentationNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, preferred_label_role, order)
    
    def create_root_node(self, xml_link: lxml.etree._Element, xml_arc: lxml.etree._Element, report_element: IReportElement) -> INetworkNode:
        nsmap = QName.get_nsmap()

        preferred_label_role = BrelLabelRole.STANDARD_LABEL
        arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
        order = 1
        arc_qname = QName.from_string(xml_arc.tag)

        link_role = xml_link.attrib.get("{" + nsmap["xlink"] + "}role")
        link_name = QName.from_string(xml_link.tag)

        if arc_role is None:
            raise ValueError(f"arcrole attribute not found on arc element {xml_arc}")
        if not isinstance(arc_role, str):
            raise TypeError(f"arcrole attribute on arc element {xml_arc} is not a string")
        if link_role is None:
            raise ValueError(f"role attribute not found on link element {xml_link}")
        if not isinstance(link_role, str):
            raise TypeError(f"role attribute on link element {xml_link} is not a string")

        return PresentationNetworkNode(report_element, [], arc_role, arc_qname, link_role, link_name, preferred_label_role, order)
    
    def update_report_elements(self, report_elements: dict[QName, IReportElement], network: INetwork) -> dict[QName, IReportElement]:
        """
        Promote abstracts to line items
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a PresentationNetwork
        @return: dict[QName, IReportElement] containing all report elements, some of which may have been promoted to line items.
        """
        if not isinstance(network, PresentationNetwork):
            raise TypeError("network must be of type PresentationNetwork")
        
        # find the nodes to promote
        nodes_to_promote: list[PresentationNetworkNode] = []
        nodes = cast(list[PresentationNetworkNode], network.get_all_nodes())
        for node in nodes:
            if isinstance(node.get_report_element(), PyBRAbstract):
                parent = next(filter(lambda x: node in x.get_children(), nodes), None)

                # promote if the node is abstract and the parent is a hypercube
                if parent is not None and isinstance(parent.get_report_element(), PyBRHypercube):
                    nodes_to_promote.append(node)
                
                hypercube_children = list(filter(lambda x: isinstance(x.get_report_element(), PyBRHypercube), node.get_children()))

                # promote if the node is abstract, it is the root and it has no hypercube children
                if parent is None and len(hypercube_children) == 0:
                    nodes_to_promote.append(node)
        
        # then promote the nodes
        for node in nodes_to_promote:
            abstract = cast(PyBRAbstract, node.get_report_element())
            line_items = PyBRLineItems(abstract.get_name(), abstract.get_labels())

            # update the report elements dict
            report_elements[line_items.get_name()] = line_items

            # update the node in the network
            node._set_report_element(line_items)
        
        return report_elements
    
    def is_physical(self) -> bool:
        return True