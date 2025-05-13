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

    role_uri = get_str_attribute(xml_element, "roleURI")

    info_element = find_element(xml_element, "link:definition")
    info = (info_element.text or "") if info_element is not None else ""

    used_ons = [used_on.text for used_on in find_elements(xml_element, "link:usedOn")]
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
) -> None:
    xml_service = context.get_xml_service()
    error_repository: ErrorRepository = context.get_error_repository()
    component_repository: ComponentRepository = context.get_component_repository()

    for schema in xml_service.get_all_etrees():
        for roletype in find_elements(schema, ".//link:roleType"):
            error_repository.upsert_on_error(
                lambda: component_repository.upsert(
                    parse_component_from_xml(context, roletype)
                )
            )
