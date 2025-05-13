"""
This module parses multiple etrees into a dict of networks.

=================

- author: Robin Schmidiger
- version: 0.20
- date: 5 April 2025

=================
"""

import json
from collections import defaultdict
from importlib.resources import files
from lxml.etree import _Element  # type: ignore
from brel.networks import *
from brel.parsers.XML.networks import parse_xml_link
from brel.parsers.utils.lxml_utils import find_elements, get_str_attribute
from brel.parsers.utils.network_utils import combine_networks
from brel.qnames.qname_utils import qname_from_str
from brel.reportelements import *
from brel.resource import *

from brel.contexts.filing_context import FilingContext
from brel.data.errors.error_repository import ErrorRepository
from brel.data.network.network_repository import NetworkRepository

# CONFIG_PATH = "brel/config/linkconfig.json"

DEBUG = False

link_config_content = files("brel.config").joinpath("linkconfig.json").read_text()
LINK_CONFIG = json.loads(link_config_content)
STANDARD_LINK_NAMES: list[str] = LINK_CONFIG["standard_link_names"]
STANDARD_RESOURCE_ROLES: list[str] = LINK_CONFIG["standard_resource_roles"]
STANDARD_LINK_ROLES: list[str] = LINK_CONFIG["standard_link_roles"]


def parse_networks_from_xmls(
    context: FilingContext,
) -> None:
    """
    Parse the networks from a list of xml trees.
    :param xml_trees: The xml trees to parse the networks from.
    :param qname_nsmap: The QNameNSMap to use for parsing.
    :param id_to_any: A mapping from xml ids to report elements, facts, and components.
    :param report_elements: The report elements to use for parsing.
    :return:
    - Mapping[str, list[INetwork]]: A mapping from link role to a list of networks.
    - list[Exception]: A list of exceptions that occurred during parsing.
    """

    error_repository: ErrorRepository = context.get_error_repository()
    network_repository: NetworkRepository = context.get_network_repository()
    xml_service = context.get_xml_service()
    networks: dict[str, list[INetwork]] = defaultdict(list)
    combined_networks: dict[str, list[INetwork]] = defaultdict(list)

    def is_standard_role(role: str) -> bool:
        return any(standard_role in role for standard_role in STANDARD_LINK_ROLES)

    link_xmls: list[_Element] = [
        element
        for xml_tree in xml_service.get_all_etrees()
        for element in find_elements(xml_tree, ".//link:*[@xlink:type='extended']")
    ]

    link_xmls.sort(
        key=lambda link: is_standard_role(
            get_str_attribute(link, qname_from_str("xlink:role", link))
        ),
        reverse=True,
    )

    # First pass: parse networks
    for link_xml in link_xmls:
        link_role = get_str_attribute(link_xml, qname_from_str("xlink:role", link_xml))

        link_networks = error_repository.upsert_on_error(
            lambda: parse_xml_link(context, link_xml)
        )
        if link_networks is None:
            continue

        networks[link_role].extend(link_networks)

    # Second pass: combine networks if they are of the same type
    for role, network_list in networks.items():
        networks_by_type: dict[type, list[INetwork]] = defaultdict(list)

        combined_network_list: list[INetwork] = []
        for network in network_list:
            if network.is_physical():
                combined_network_list.append(network)
            else:
                networks_by_type[type(network)].append(network)

        for network_type_list in networks_by_type.values():
            combined_network_list.append(combine_networks(network_type_list))

        combined_networks[role] = combined_network_list

    for role, network_list in combined_networks.items():
        for network in network_list:
            network_repository.upsert(role, network)
