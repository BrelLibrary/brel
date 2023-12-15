import lxml.etree

from brel import QName, QNameNSMap
from brel.networks import *
from brel.reportelements import *
from brel.resource import *

from typing import cast
from collections import defaultdict
import validators

# TODO: change this
from .xml_extended_link_parser import parse_xml_link

DEFAULT_LINK_ROLE = "http://www.xbrl.org/2003/role/link"

def networks_from_xmls(
        xml_trees: list[lxml.etree._ElementTree],
        qname_nsmap: QNameNSMap,
        report_elements: dict[QName, IReportElement]
        ) -> dict[str, list[INetwork]]:
    
    nsmap = qname_nsmap.get_nsmap()

    # first, we want to get all extended links in all xml trees
    # we do this by going over all xml trees and getting all extended links
    links = []
    for xml_tree in xml_trees:
        all_links = xml_tree.findall(".//link:*[@xlink:type='extended']", namespaces=nsmap)
        links.extend(all_links)
    
    # then we want to parse the extended links with the default role first.
    # This is because some extended links may rely on labels that are defined in other extended links.
    # Specifically, the presentation networks rely on labels that are defined in the label networks.
    # Label networks have the default link role.
    links.sort(key=lambda link: link.get("{" + nsmap["xlink"] + "}role") == DEFAULT_LINK_ROLE, reverse=True)

    networks: dict[str, list[INetwork]] = defaultdict(list)

    # go over all extended links in all xml trees
    for xml_link in links:
        # get the link role
        link_role = xml_link.get("{" + nsmap["xlink"] + "}role", None)
        if link_role is None:
            raise ValueError(f"the link element {xml_link} does not have a xlink:role attribute")
        
        # Check if the link_role is a valid absolute URI
        if not isinstance(link_role, str) and not validators.url(link_role):
            raise ValueError(f"the link element {xml_link} has an invalid xlink:role attribute '{link_role}'. The xlink:role attribute must be a valid absolute URI.")
        
        # According to the XBRL Generic Links spec, if the xlink:role is not the default link role, 
        # then the ancestor linkbase must have a roleRef with the roleURI equal to the xlink:role.
        # this roleRef's href must point to a role definition that has a usedOn attribute that contains the link element's name.
        
        # if the link role is not the default link role, get the roleRef
        if link_role != DEFAULT_LINK_ROLE:
            # first, get the parent linkbase
            linkbase: lxml.etree._Element | None = xml_link.getparent()
            while linkbase is not None and linkbase.tag != f"{{{nsmap['link']}}}linkbase":
                linkbase = linkbase.getparent()
            
            if linkbase is None:
                raise ValueError(f"the link element with xlink:role='{link_role}' does not have a parent linkbase. All links with a non-default xlink:role must be in a linkbase.")
            
            # find the roleRef in the linkbase
            role_ref = linkbase.find(f".//link:roleRef[@roleURI='{link_role}']", namespaces=nsmap)
            if role_ref is None:
                # TODO: throw a xbrlgene:missingRoleRefForLinkRole
                raise ValueError(f"the link element with xlink:role='{link_role}' does not have a roleRef in its parent linkbase. All links with a non-default xlink:role must be in a linkbase.")
            
            # get the href attribute
            href = role_ref.get("{" + nsmap["xlink"] + "}href", None)
            if href is None:
                raise ValueError(f"the roleRef with roleURI='{link_role}' does not have a href attribute")
            
            # get the component name
            _, component_name = href.split("#")
            if component_name == "":
                raise ValueError(f"the roleRef with roleURI='{link_role}' has an invalid href attribute href='{href}'")
            
        else:
            component_name = "default link role"
        
        # parse the network and update the report elements
        link_networks, report_elements = parse_xml_link(xml_link, qname_nsmap, report_elements)

        # add the presentation network to the networks dict
        networks[component_name].extend(link_networks)
        
    return networks

                
                



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
            link_networks, report_elements = parse_xml_link(xml_link, qname_nsmap, report_elements)

            if link_networks is not None:
                # get the component name
                component_name = link_to_component_name(xml_link)

                # add the presentation network to the networks dict
                networks[component_name].extend(link_networks)
        
    return networks
