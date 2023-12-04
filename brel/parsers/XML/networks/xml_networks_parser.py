import lxml.etree

from brel import QName
from brel.networks import *
from brel.reportelements import *
from brel.resource import *

from typing import cast
from collections import defaultdict

# TODO: change this
from .xml_linkbase_parser import parse_xml_link

def networks_from_xmls(
        xml_trees: list[lxml.etree._ElementTree],
        report_elements: dict[QName, IReportElement]
        ) -> dict[str, list[INetwork]]:
    
    nsmap = QName.get_nsmap()

    networks: dict[str, list[INetwork]] = defaultdict(list)

    def link_to_component_name(link: lxml.etree._Element) -> str:
        """
        Given a link element, get the component name.
        @param link: The link element.
        @return: The component name as a string.
        @raise ValueError: If the roleRef cannot be found or if the roleRef has either no href attribute or an invalid href attribute.
        """

        link_role = link.get("{" + nsmap["xlink"] + "}role")

        if link_role is None:
            raise ValueError("the link element does not have a xlink:role attribute")
        
        # TODO: TODO: think about this
        if "/role/link" in link_role:
            return "labels_networks" 

        role_ref = xml_tree.find(f".//link:roleRef[@roleURI='{link_role}']", namespaces=nsmap)
        if role_ref is None:
            raise ValueError(f"the roleRef with roleURI='{link_role}' could not be found")
        
        href = role_ref.get("{" + nsmap["xlink"] + "}href")
        if href is None:
            raise ValueError(f"the roleRef with roleURI='{link_role}' does not have a href attribute")
        _, component_name = href.split("#")

        if component_name == "":
            raise ValueError(f"the roleRef with roleURI='{link_role}' has an invalid href attribute href='{href}'")

        return component_name
    
    for xml_tree in xml_trees:
        
        # check if root is a linkbase
        root = xml_tree.getroot()
        if root.tag == f"{{{nsmap['link']}}}linkbase":
            xml_links = root.findall("link:*[@xlink:role]", namespaces=nsmap)
        else:
            xml_links = xml_tree.findall(".//link:linkbase/*[@xlink:role]", namespaces=nsmap)

        for xml_link in xml_links:
            # parse the network and update the report elements
            link_networks, report_elements = parse_xml_link(xml_link, report_elements)

            if link_networks is not None:
                # get the component name
                component_name = link_to_component_name(xml_link)

                # add the presentation network to the networks dict
                networks[component_name].extend(link_networks)
        
    return networks
