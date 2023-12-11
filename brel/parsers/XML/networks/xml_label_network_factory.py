import lxml
import lxml.etree
from typing import cast
from brel import QName
from brel.networks import INetwork, INetworkNode, LabelNetwork, LabelNetworkNode
from brel.reportelements import IReportElement
from brel.resource import BrelLabel, IResource

# TODO: change this
from .i_xml_network_factory import IXMLNetworkFactory

class LabelNetworkFactory(IXMLNetworkFactory):
    def create_network(self, xml_link_element: lxml.etree._Element, roots: list[INetworkNode]) -> INetwork:
        nsmap = QName.get_nsmap()

        link_role = xml_link_element.get(f"{{{nsmap['xlink']}}}role", None)
        link_qname = QName.from_string(xml_link_element.tag)

        if len(roots) == 0:
            raise ValueError("roots must not be empty")
        if not all(isinstance(root, LabelNetworkNode) for root in roots):
            raise TypeError("roots must all be of type LabelNetworkNode")
        if link_role is None:
            raise ValueError(f"linkrole attribute not found on link element {xml_link_element}")
        
        roots_cast = cast(list[LabelNetworkNode], roots)

        return LabelNetwork(roots_cast, link_role, link_qname)
    
    def create_node(self, xml_link: lxml.etree._Element, xml_referenced_element: lxml.etree._Element, xml_arc: lxml.etree._Element | None, points_to: IReportElement|IResource) -> INetworkNode:
        nsmap = QName.get_nsmap()

        label = xml_referenced_element.attrib.get(f"{{{nsmap['xlink']}}}label", None)
        if label is None:
            raise ValueError(f"label attribute not found on referenced element {xml_referenced_element}")

        if xml_arc is None:
            # the node is not connected to any other node
            arc_role = "unknown"
            arc_qname = QName.from_string("link:unknown")
        elif xml_arc.get(f"{{{nsmap['xlink']}}}from", None) == label:
            # the node is a root
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            arc_qname = QName.from_string(xml_arc.tag)
        elif xml_arc.get(f"{{{nsmap['xlink']}}}to", None) == label:
            # the node is an inner node
            arc_role = xml_arc.attrib.get("{" + nsmap["xlink"] + "}arcrole")
            arc_qname = QName.from_string(xml_arc.tag)
        else:
            raise ValueError(f"referenced element {xml_referenced_element} is not connected to arc {xml_arc}")
        
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
        if not isinstance(points_to, BrelLabel) and not isinstance(points_to, IReportElement):
            raise TypeError(f"'points_to' must be of type BrelLabel or IReportElement, not {type(points_to)}")
        
        return LabelNetworkNode(points_to, arc_role, arc_qname, link_role, link_name)
    
    def update_report_elements(self, report_elements: dict[QName, IReportElement], label_network: INetwork) -> dict[QName, IReportElement]:
        """
        Label networks add the labels to the report elements
        @param report_elements: dict[QName, IReportElement] containing all report elements
        @param network: INetwork containing the network. Must be a CalculationNetwork
        @return: dict[QName, IReportElement] containing all report elements. same as the report_elements parameter
        """

        # label networks tend to be nearly flat. The roots are the report element nodes and their children are label nodes
        for root in label_network.get_roots():
            if not isinstance(root, LabelNetworkNode):
                raise TypeError("roots must all be of type LabelNetworkNode")
            if not root.is_a() == "report element":
                raise ValueError(f"root {root} is not a report element")
            
            report_element = root.get_report_element()
            for label_node in root.get_children():
                if not isinstance(label_node, LabelNetworkNode):
                    raise TypeError("children must all be of type LabelNetworkNode")
                if not label_node.is_a() == "resource":
                    raise ValueError(f"child {label_node} is not a resource")
                
                label = label_node.get_resource()
                if not isinstance(label, BrelLabel):
                    raise TypeError(f"label {label} is not a BrelLabel. It is of type {type(label)}")
                
                report_element._add_label(label)

        return report_elements
    
    def is_physical(self) -> bool:
        return True