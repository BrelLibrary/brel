"""
This module parses the components from the xbrl instance.
It does not parse the networks, but it links components to networks.

=================

- author: Robin Schmidiger
- version: 0.5
- date: 07 January 2024

=================
"""
import lxml
import lxml.etree

from brel.reportelements import IReportElement
from brel import QName, QNameNSMap, Component
from brel.networks import (
    PresentationNetwork,
    CalculationNetwork,
    DefinitionNetwork,
    INetwork,
)

from typing import Callable


def parse_component_from_xml(
    xml_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    presentation_network: None | PresentationNetwork = None,
    calculation_network: None | CalculationNetwork = None,
    definition_network: None | DefinitionNetwork = None,
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
        raise ValueError(
            "The roleURI attribute is missing from the link:roleType element"
        )

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
    used_ons = [
        used_on.text
        for used_on in xml_element.findall("link:usedOn", namespaces=nsmap)
    ]
    if (
        presentation_network is not None
        and "link:presentationLink" not in used_ons
    ):
        raise ValueError(
            f"A presentation network is not allowed for the component with id '{uri}', but one was passed."
        )
    if (
        calculation_network is not None
        and "link:calculationLink" not in used_ons
    ):
        raise ValueError(
            f"A calculation network is not allowed for the component with id '{uri}', but one was passed."
        )
    if (
        definition_network is not None
        and "link:definitionLink" not in used_ons
    ):
        raise ValueError(
            f"A definition network is not allowed for the component with id '{uri}', but one was passed."
        )

    return Component(
        uri,
        info,
        presentation_network,
        calculation_network,
        definition_network,
    )


def parse_components_xml(
    schemas: list[lxml.etree._ElementTree],
    networks: dict[str | None, list[INetwork]],
    report_elements: dict[QName, IReportElement],
    qname_nsmap: QNameNSMap,
) -> tuple[list[Component], dict[QName, IReportElement]]:
    """
    Parse the components.
    :param schemas: The xbrl schema xml trees
    :param networks: The networks as a dictionary of roleID -> list of networks. Networks that belong to the default role have roleID None.
    :param report_elements: The report elements as a dictionary of QName -> IReportElement
    :param qname_nsmap: The QNameNSMap
    :return: a tuple containing:
        - A list of all the components in the filing.
        - A dictionary of all the report elements in the filing. These might have been altered by the components. More specifically, some abstracts might have been promoted to line items.
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

            definition_element = roletype.find(
                "link:definition", namespaces=nsmap
            )
            if definition_element is None:
                raise ValueError(
                    f"The role with roleURI {roleURI} does not have a definition element"
                )

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
            if (
                not roleID_strippped.isidentifier()
                or roleID.startswith("-")
                or roleID.startswith(".")
            ):
                raise ValueError(f"roleID {roleID} is not a valid NCName")

            # TODO: give all the networks associated with a component to the component instead of pre-filtering them here
            # Maybe a component has more than just presentation, definition and calculation networks
            # Find the networks that belong to the component
            presentation_network = next(
                (
                    x
                    for x in networks[roleID]
                    if isinstance(x, PresentationNetwork)
                ),
                None,
            )
            calculation_network = next(
                (
                    x
                    for x in networks[roleID]
                    if isinstance(x, CalculationNetwork)
                ),
                None,
            )
            # definition_network = next((x for x in networks[roleID] if isinstance(x, DefinitionNetwork)), None)

            # reconstruct the definition network from the physical definition networks
            # get the physical definition networks
            definition_network = next(
                (
                    x
                    for x in networks[roleID]
                    if isinstance(x, DefinitionNetwork) and not x.is_physical()
                ),
                None,
            )

            component = parse_component_from_xml(
                roletype,
                qname_nsmap,
                presentation_network,
                calculation_network,
                definition_network,
            )
            components.append(component)

    return components, report_elements
