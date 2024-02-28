"""
This module parses the components from the xbrl instance.
It does not parse the networks, but it links components to networks.

=================

- author: Robin Schmidiger
- version: 0.7
- date: 31 January 2024

=================
"""

from typing import Callable, Mapping, Iterable, Tuple

import lxml
import lxml.etree

from brel import Component, QName, QNameNSMap
from brel.networks import (
    CalculationNetwork,
    DefinitionNetwork,
    INetwork,
    PresentationNetwork,
)
from brel.reportelements import IReportElement
from brel.parsers.utils import get_str


def parse_component_from_xml(
    xml_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    networks: Iterable[INetwork],
) -> Component:
    """
    Creates a single Component from an lxml.etree._Element.
    :param xml_element: The lxml.etree._Element to create the Component from.
    :param qname_nsmap: The QNameNSMap
    :param presentation_network: The presentation network of the component. None if the component has no presentation network or if the network is empty.
    :param calculation_network: The calculation network of the component. None if the component has no calculation network or if the network is empty.
    :param definition_network: The definition network of the component. None if the component has no definition network or if the network is empty.
    :returns: The newly created Component.
    """

    uri = xml_element.get("roleURI", None)
    nsmap = qname_nsmap.get_nsmap()

    if uri is None:
        raise ValueError("The roleURI attribute is missing from the link:roleType element")

    # the info is in a child element of the xml_element called "definition"
    try:
        info_element = xml_element.find("link:definition", namespaces=nsmap)
        if info_element is None:
            info = ""
        else:
            info = info_element.text or ""
    except AttributeError:
        info = ""

    # check the usedOn elements
    used_ons = [used_on.text for used_on in xml_element.findall("link:usedOn", namespaces=nsmap)]

    if "link:presentationLink" not in used_ons and any(map(lambda n: isinstance(n, PresentationNetwork), networks)):
        raise ValueError(f"Component {uri} has presentation networks, but no appropriate usedOn element")
    if "link:calculationLink" not in used_ons and any(map(lambda n: isinstance(n, CalculationNetwork), networks)):
        raise ValueError(f"Component {uri} has calculation networks, but no appropriate usedOn element")
    if "link:definitionLink" not in used_ons and any(map(lambda n: isinstance(n, DefinitionNetwork), networks)):
        raise ValueError(f"Component {uri} has definition networks, but no appropriate usedOn element")

    return Component(uri, info, list(networks))


def parse_components_xml(
    schemas: Iterable[lxml.etree._ElementTree],
    networks: Mapping[str, Iterable[INetwork]],
    qname_nsmap: QNameNSMap,
) -> Tuple[list[Component], list[Exception]]:
    """
    Parse the components.
    :param schemas: The xbrl schema xml trees
    :param networks: The networks as a dictionary of roleURI -> list of networks. Networks that belong to the default role have roleID None.
    :param qname_nsmap: The QNameNSMap
    :returns:
    - list[Component]: All the components in the filing.
    - list[Exception]: All the exceptions that occurred during parsing.
    """
    nsmap = qname_nsmap.get_nsmap()

    components: list[Component] = []
    errors: list[Exception] = []

    # Iterate over all files that may contain components. Components are defined in the schemas
    for schema in schemas:
        # get all roleTypes in the schema. They correspond to the components
        roletypes = schema.findall(".//link:roleType", namespaces=nsmap)
        for roletype in roletypes:
            # Read the component information from the roleType xml element
            # roleURI = roletype.get("roleURI")
            # roleID = roletype.get("id")

            # if roleURI is None:
            #     raise ValueError(f"roleURI for role {roleID} is None")

            # if roleID is None:
            #     raise ValueError(f"roleID for role {roleURI} is None")
            try:
                roleURI = get_str(roletype, "roleURI")
                roleID = get_str(roletype, "id")
            except Exception as e:
                errors.append(e)
                continue

            # check if the role id is a valid NCName
            # NCName is defined in https://www.w3.org/TR/xml-names/#NT-NCName
            # NCNames are similar to python identifiers, except that they might contain '.' and '-' (not in the beginning)
            roleID_stripped = roleID.replace(".", "").replace("-", "")
            if not roleID_stripped.isidentifier() or roleID.startswith("-") or roleID.startswith("."):
                # raise ValueError(f"roleID {roleID} is not a valid NCName")
                errors.append(ValueError(f"roleID {roleID} is not a valid NCName"))
                continue

            try:
                component = parse_component_from_xml(
                    roletype,
                    qname_nsmap,
                    networks[roleURI],
                )
                components.append(component)
            except Exception as e:
                errors.append(e)

    return components, errors
