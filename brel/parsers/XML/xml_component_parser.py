import os
import lxml
import lxml.etree

from brel.reportelements import IReportElement
from brel import QName, QNameNSMap, Component
from brel.networks import PresentationNetwork, CalculationNetwork, DefinitionNetwork, INetwork
from collections import defaultdict

# change this

def parse_components_xml(
        schemas: list[lxml.etree._ElementTree],
        networks: dict[str, list[INetwork]],
        report_elements: dict[QName, IReportElement],
        qname_nsmap: QNameNSMap
        ) -> tuple[list[Component], dict[QName, IReportElement]]:
    """
    Parse the components.
    @return: 
        - A list of all the components in the filing.
        - A dictionary of all the report elements in the filing. These might have been altered by the components.
    """

    nsmap = qname_nsmap.get_nsmap()
        
    components: list[Component] = []

    # Iterate over all files that may contain components. Components are defined in the schemas
    for schema in schemas:
        # get all roleTypes in the schema. They correspond to the components
        roletypes = schema.findall(".//link:roleType", namespaces=nsmap)
        for roletype in roletypes:
            
            # Read the component information from the roleType xml element
            roleURI = roletype.get("roleURI")
            roleID = roletype.get("id")
            
            definition_element = roletype.find("link:definition", namespaces=nsmap)
            if definition_element is None:
                raise ValueError(f"The role with roleURI {roleURI} does not have a definition element")
            
            definition = definition_element.text

            if definition is None:
                definition = ""
            
            if roleURI is None:
                raise ValueError(f"roleURI for role {roleID} is None")
            
            if roleID is None:
                raise ValueError(f"roleID for role {roleURI} is None")
            
            # check if the role id is a valid NCName
            # NCName is defined in https://www.w3.org/TR/xml-names/#NT-NCName
            # NCNames are similar to python identifiers, except that they might contain '.' and '-' (not in the beginning)
            roleID_strippped = roleID.replace(".", "").replace("-", "")
            if not roleID_strippped.isidentifier() or roleID.startswith("-") or roleID.startswith("."):
                raise ValueError(f"roleID {roleID} is not a valid NCName")
            
            # Find the networks that belong to the component
            presentation_network = next((x for x in networks[roleID] if isinstance(x, PresentationNetwork)), None)
            calculation_network = next((x for x in networks[roleID] if isinstance(x, CalculationNetwork)), None)
            # definition_network = next((x for x in networks[roleID] if isinstance(x, DefinitionNetwork)), None)

            # reconstruct the definition network from the physical definition networks
            # get the physical definition networks
            definition_network = next((x for x in networks[roleID] if isinstance(x, DefinitionNetwork) and not x.is_physical()), None)

            component = Component.from_xml(roletype, qname_nsmap, presentation_network, calculation_network, definition_network)
            components.append(component)

    return components, report_elements