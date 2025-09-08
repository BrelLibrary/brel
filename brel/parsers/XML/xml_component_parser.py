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
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.networks import (
    CalculationNetwork,
    DefinitionNetwork,
    PresentationNetwork,
)
from brel.contexts.filing_context import FilingContext
from brel.data.errors.error_repository import ErrorRepository
from brel.data.component.component_repository import ComponentRepository
from brel.data.network.network_repository import NetworkRepository
from brel.parsers.utils.lxml_utils import find_element, find_elements, get_str_attribute


def parse_component_from_xml(
    context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
) -> Component:
    network_repository: NetworkRepository = context.get_network_repository()
    error_repository: ErrorRepository = context.get_error_repository()

    role_uri = get_str_attribute(xml_element, "roleURI")

    info_element = find_element(xml_element, "link:definition")
    info = (info_element.text or "") if info_element is not None else ""

    used_ons = [used_on.text for used_on in find_elements(xml_element, "link:usedOn")]
    networks_in_component = network_repository.get_by_linkrole(role_uri)

    if "link:presentationLink" not in used_ons and any(
        map(lambda n: isinstance(n, PresentationNetwork), networks_in_component)
    ):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.PRESENTATION_NETWORK_IN_COMPONENT_WITHOUT_USEDON_ELEMENT,
                xml_element,
                linkrole_uri=role_uri,
            )
        )

    if "link:calculationLink" not in used_ons and any(
        map(lambda n: isinstance(n, CalculationNetwork), networks_in_component)
    ):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.CALCULATION_NETWORK_IN_COMPONENT_WITHOUT_USEDON_ELEMENT,
                xml_element,
                linkrole_uri=role_uri,
            )
        )

    if "link:definitionLink" not in used_ons and any(
        map(lambda n: isinstance(n, DefinitionNetwork), networks_in_component)
    ):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.DEFINITION_NETWORK_IN_COMPONENT_WITHOUT_USEDON_ELEMENT,
                xml_element,
                linkrole_uri=role_uri,
            )
        )

    presentation_networks = [
        network
        for network in networks_in_component
        if isinstance(network, PresentationNetwork)
    ]
    calculation_networks = [
        network
        for network in networks_in_component
        if isinstance(network, CalculationNetwork)
    ]
    definition_networks = [
        network
        for network in networks_in_component
        if isinstance(network, DefinitionNetwork)
        and not network.is_physical()
    ]

    if len(presentation_networks) > 1:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.MULTIPLE_PRESENTATION_NETWORKS_IN_COMPONENT,
                xml_element,
                linkrole_uri=role_uri,
            )
        )
    if len(calculation_networks) > 1:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.MULTIPLE_CALCULATION_NETWORKS_IN_COMPONENT,
                xml_element,
                linkrole_uri=role_uri,
            )
        )
    if len(definition_networks) > 1:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.MULTIPLE_DEFINITION_NETWORKS_IN_COMPONENT,
                xml_element,
                linkrole_uri=role_uri,
            )
        )

    presentation_network = (
        presentation_networks[0] if len(presentation_networks) >= 1 else None
    )
    calculation_network = (
        calculation_networks[0] if len(calculation_networks) >= 1 else None
    )
    definition_network = (
        definition_networks[0] if len(definition_networks) >= 1 else None
    )

    return Component(
        role_uri, info, presentation_network, calculation_network, definition_network
    )


def parse_components_xml(
    context: FilingContext,
) -> None:
    xml_service = context.get_xml_service()
    component_repository: ComponentRepository = context.get_component_repository()

    for schema in xml_service.get_all_etrees():
        for roletype in find_elements(
            schema,
            ".//link:roleType",
            namespaces={"link": "http://www.xbrl.org/2003/linkbase"},
        ):
            component_repository.upsert(parse_component_from_xml(context, roletype))
