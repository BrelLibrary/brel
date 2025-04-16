"""
This module parses the components from the xbrl instance.
It does not parse the networks, but it links components to networks.

=================

- author: Robin Schmidiger
- version: 0.8
- date: 15 April 2025

=================
"""

from typing import Iterable

import lxml
import lxml.etree

from brel import Component
from brel.networks import (
    CalculationNetwork,
    DefinitionNetwork,
    PresentationNetwork,
)
from brel.parsers.utils import get_str_attribute
from brel.contexts.filing_context import FilingContext
from brel.data.errors.error_repository import ErrorRepository
from brel.data.component.component_repository import ComponentRepository
from brel.data.network.network_repository import NetworkRepository


def parse_component_from_xml(
    context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
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
    network_repository: NetworkRepository = context.get_network_repository()
    nsmap = context.get_nsmap().as_dict()

    role_uri = get_str_attribute(xml_element, "roleURI")

    try:
        info_element = xml_element.find("link:definition", namespaces=nsmap)
        if info_element is None:
            info = ""
        else:
            info = info_element.text or ""
    except AttributeError:
        info = ""

    used_ons = [
        used_on.text for used_on in xml_element.findall("link:usedOn", namespaces=nsmap)
    ]
    networks_in_component = network_repository.get(role_uri)

    if "link:presentationLink" not in used_ons and any(
        map(lambda n: isinstance(n, PresentationNetwork), networks_in_component)
    ):
        raise ValueError(
            f"Component {role_uri} has presentation networks, but no appropriate usedOn element"
        )
    if "link:calculationLink" not in used_ons and any(
        map(lambda n: isinstance(n, CalculationNetwork), networks_in_component)
    ):
        raise ValueError(
            f"Component {role_uri} has calculation networks, but no appropriate usedOn element"
        )
    if "link:definitionLink" not in used_ons and any(
        map(lambda n: isinstance(n, DefinitionNetwork), networks_in_component)
    ):
        raise ValueError(
            f"Component {role_uri} has definition networks, but no appropriate usedOn element"
        )

    return Component(role_uri, info, networks_in_component)


def parse_components_xml(
    context: FilingContext,
    schemas: Iterable[lxml.etree._ElementTree],  # type: ignore
) -> None:
    """
    Parse the components.
    :param schemas: The xbrl schema xml trees
    :param networks: The networks as a dictionary of roleURI -> list of networks. Networks that belong to the default role have roleID None.
    :param qname_nsmap: The QNameNSMap
    :returns:
    - list[Component]: All the components in the filing.
    - list[Exception]: All the exceptions that occurred during parsing.
    """

    nsmap = context.get_nsmap().as_dict()
    error_repository: ErrorRepository = context.get_error_repository()
    component_repository: ComponentRepository = context.get_component_repository()

    for schema in schemas:
        roletypes = schema.findall(".//link:roleType", namespaces=nsmap)
        for roletype in roletypes:
            error_repository.upsert_on_error(
                lambda: component_repository.upsert(
                    parse_component_from_xml(context, roletype)
                )
            )
