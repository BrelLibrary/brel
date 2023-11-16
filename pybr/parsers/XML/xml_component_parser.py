import os
import lxml
import lxml.etree

from pybr.reportelements import IReportElement
from pybr import QName, PyBRComponent
from pybr.networks import PresentationNetwork, CalculationNetwork, DefinitionNetwork, INetwork
from collections import defaultdict

# change this
from .networks.xml_network_parser import network_from_xml

def parse_components_xml(
        schemas: list[lxml.etree._ElementTree],
        network_files: list[lxml.etree._ElementTree],
        report_elements: dict[QName, IReportElement]
        ) -> tuple[list[PyBRComponent], dict[QName, IReportElement]]:
    """
    Parse the components.
    @return: 
        - A list of all the components in the filing.
        - A dictionary of all the report elements in the filing. These might have been altered by the components.
    """

    # The parsing of the components is done in two passes:
    # Step 1. Parse the networks
    # Step 2. Parse the components. If a component references a network, the network is already parsed and can be used

    nsmap = QName.get_nsmap()
    
    # Step 1. Parse the networks
    # Iterate over all files that may contain networks
    networks: dict[str, list] = defaultdict(list)

    def link_to_component_name(link: lxml.etree._Element) -> str:
        link_role = link.get("{" + nsmap["xlink"] + "}role")
        role_ref = xml_tree.find(f".//link:roleRef[@roleURI='{link_role}']", namespaces=nsmap)
        href = role_ref.get("{" + nsmap["xlink"] + "}href")
        _, component_name = href.split("#")

        return component_name

    for xml_tree in network_files + schemas:
        
        # check if root is a linkbase
        root = xml_tree.getroot()
        if root.tag == f"{{{nsmap['link']}}}linkbase":
            xml_links = root.findall("link:*[@xlink:role]", namespaces=nsmap)
        else:
            xml_links = xml_tree.findall(".//link:linkbase/*[@xlink:role]", namespaces=nsmap)
            if len(xml_links) > 0:
                print("WARNING: found non-root linkbase")
                print(xml_links)

        for xml_link in xml_links:
            # parse the network and update the report elements
            network, report_elements = network_from_xml(xml_link, report_elements)

            if network is not None:
                # get the component name
                component_name = link_to_component_name(xml_link)

                # add the presentation network to the networks dict
                networks[component_name].append(network)
        
    # Step 2. Parse the components
    components: list[PyBRComponent] = []

    # Iterate over all files that may contain components. Components are defined in the schemas
    for schema in schemas:
        # get all roleTypes in the schema. They correspond to the components
        roletypes = schema.findall(".//link:roleType", namespaces=nsmap)
        for roletype in roletypes:
            
            # Read the component information from the roleType xml element
            roleURI = roletype.get("roleURI")
            roleID = roletype.get("id")
            definition = roletype.find("link:definition", namespaces=nsmap).text

            if definition is None:
                definition = ""
            
            if roleURI is None:
                raise ValueError(f"roleURI for role {roleID} is None")
            
            if roleID is None:
                raise ValueError(f"roleID for role {roleURI} is None")
            
            
            # Find the networks that belong to the component
            presentation_network = next((x for x in networks[roleID] if isinstance(x, PresentationNetwork)), None)
            calculation_network = next((x for x in networks[roleID] if isinstance(x, CalculationNetwork)), None)
            definition_network = next((x for x in networks[roleID] if isinstance(x, DefinitionNetwork)), None)

            component = PyBRComponent.from_xml(roletype, presentation_network, calculation_network, definition_network)
            components.append(component)

    return components, report_elements