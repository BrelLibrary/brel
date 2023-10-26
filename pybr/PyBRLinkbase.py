import lxml
import lxml.etree
from typing import TypeVar, Generic
from pybr import QName, PyBRConceptCharacteristic

class PyBRLinkbase:
    """
    A class representing a linkbase. It acts like a graph.
    """

    def __init__(self) -> None:
        self.__children: list[PyBRConceptCharacteristic] = []
        self.__parents: list[PyBRConceptCharacteristic] = []
    
    def add_child(self, child: "PyBRLinkbase"):
        """
        Add a child to the linkbase
        """
        # check if the child is already in the children list
        if child in self.__children:
            return

        self.__children.append(child)
        child.add_parent(self)
    
    def add_parent(self, parent: "PyBRLinkbase"):
        """
        Add a parent to the linkbase
        """
        # check if the parent is already in the parents list
        if parent in self.__parents:
            return

        self.__parents.append(parent)
        parent.add_child(self)

    
    @classmethod
    def presentation_network_from_xml(cls, xml_xtree: lxml.etree._Element) -> list["PyBRLinkbase"]:
        """
        Creates a presentation network from an XML tree
        A presentation network is just a list of PyBRLinkbase objects
        """
        nsmap = QName.get_nsmap()

        # first iterate over all presentationLink elements
        # presentation_links = xml_xtree.findall(".//{*}presentationLink")
        presentation_links = xml_xtree.findall(".//link:presentationLink", namespaces=nsmap)
        presentation_network = []
        print("computing presentation network")
        for presentation_link in presentation_links:
            # create a PyBRLinkbase from the presentationLink element
            # iterate over all presentationArc elements
            # add the PyBRLinkbase to the presentation network
            edges = []
            presentation_arcs = presentation_link.findall(".//{*}presentationArc", )
            for arc in presentation_arcs:
                # print(arc.attrib)
                # edges.append((arc.get("{*}from"), arc.get("{*}to")))
                # get the from attribute from the arc
                from_attr = arc.get(f"link:from")
                # get the to attribute from the arc
                to_attr = arc.get(f"link:to")
                edges.append((from_attr, to_attr))
                            
            print(edges)

            # for each source\target in the edges, get the corresponding concepts
            for source_tag, target_tag in edges:
                # find the corresponding locators
                source_locator = presentation_link.find(f".//{{*}}loc[@xlink:href='{source_tag}']")
                target_locator = presentation_link.find(f".//{{*}}loc[@xlink:href='{target_tag}']")

                # get the concept qname


