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
import time
from importlib.resources import files
from typing import Iterable

import lxml.etree

from brel.networks import *
from brel.parsers.XML.networks import parse_xml_link
from brel.parsers.utils.lxml_utils import get_str_attribute, get_str_tag
from brel.reportelements import *
from brel.resource import *

from brel.parsers.utils import combine_networks
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
    xml_trees: Iterable[lxml.etree._ElementTree],
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

    # TODO rework this whole function
    nsmap = context.get_nsmap().as_dict()
    error_repository: ErrorRepository = context.get_error_repository()

    # first, we want to get all extended links in all xml trees
    # we do this by going over all xml trees and getting all extended links
    if DEBUG:  # pragma: no cover
        start_time = time.time()

    links = []
    for xml_tree in xml_trees:
        all_links = xml_tree.findall(
            ".//link:*[@xlink:type='extended']", namespaces=nsmap
        )
        links.extend(all_links)

    if DEBUG:  # pragma: no cover
        end_time = time.time()
        print(
            f"Found {len(links)} extended links in {end_time - start_time:.2f} seconds"
        )
        start_time = time.time()

    # then we want to parse the extended links with the default role first.
    # This is because some extended links may rely on labels that are defined in other extended links.
    # Specifically, the presentation networks rely on labels that are defined in the label networks.
    # Label networks have the default link role.
    def is_standard_role(role: str) -> bool:
        return any(standard_role in role for standard_role in STANDARD_LINK_ROLES)

    links.sort(
        key=lambda link: is_standard_role(link.get("{" + nsmap["xlink"] + "}role", "")),
        reverse=True,
    )

    networks: dict[str, list[INetwork]] = defaultdict(list)

    if DEBUG:  # pragma: no cover
        end_time = time.time()
        print(f"Sorted the extended links in {end_time - start_time:.2f} seconds")

    # go over all extended links in all xml trees
    for xml_link in links:
        link_role = error_repository.upsert_on_error(
            lambda: get_str_attribute(xml_link, f"{{{nsmap['xlink']}}}role")
        )
        link_name = get_str_tag(xml_link)

        if link_role is None:
            continue

        # According to the XBRL Generic Links spec, if the xlink:role is not the default link role,
        # then the ancestor linkbase must have a roleRef with the roleURI equal to the xlink:role.
        # this roleRef's href must point to a role definition that has a usedOn attribute that contains the link element's name.
        # rolerefs are only required for standard links and standard resources.
        # http://www.xbrl.org/specification/xbrl-2.1/rec-2003-12-31/xbrl-2.1-rec-2003-12-31+corrected-errata-2013-02-20.html#_3.5.2.4

        # check the integrity of all xlink:role attributes
        # If the xlink:role is NOT a standard link role and NOT a standard resource role,
        # And if the link name is a standard link name,
        # Then the ancestor linkbase needs to have a roleRef with the roleURI equal to the xlink:role.

        link_role_elems = xml_link.findall(".//*[@xlink:role]", namespaces=nsmap) + [
            xml_link
        ]

        if DEBUG:  # pragma: no cover
            print(f"The link has {len(link_role_elems)} elements")
        for link_role_elem in link_role_elems:
            role = error_repository.upsert_on_error(
                lambda: get_str_attribute(link_role_elem, f"{{{nsmap['xlink']}}}role")
            )
            if role is None:
                continue

            # check if the role is a standard role
            if any(standard_role in role for standard_role in STANDARD_LINK_ROLES):
                continue

            # check if the role is a standard resource role
            if any(standard_role in role for standard_role in STANDARD_RESOURCE_ROLES):
                continue

            # check if the link name is a standard link name
            if any(
                standard_link_name in link_name
                for standard_link_name in STANDARD_LINK_NAMES
            ):
                # first, get the parent linkbase
                linkbase: lxml.etree._Element | None = xml_link.getparent()
                while (
                    linkbase is not None
                    and linkbase.tag != f"{{{nsmap['link']}}}linkbase"
                ):
                    linkbase = linkbase.getparent()

                if linkbase is None:
                    raise ValueError(
                        f"the element {link_role_elem} does not have a parent linkbase. All elements with an xlink:role must be in a linkbase."
                    )

                # find the roleRef in the linkbase
                role_ref = linkbase.find(
                    f".//link:roleRef[@roleURI='{role}']", namespaces=nsmap
                )

                if role_ref is None:
                    raise ValueError(
                        f"the linkbase {linkbase} does not have a roleRef with the roleURI '{role}'. All roleRefs must have a roleURI attribute."
                    )

                # read the component name from the xlink:href of the roleRef
                href = role_ref.get(f"{{{nsmap['xlink']}}}href", None)
                if href is None:
                    raise ValueError(
                        f"the roleRef {role_ref} does not have a href attribute. All roleRefs must have a href attribute."
                    )

        # parse the network and update the report elements
        link_networks = error_repository.upsert_on_error(
            lambda: parse_xml_link(context, xml_link)
        )
        if link_networks is None:
            continue

        networks[link_role].extend(link_networks)

    # Do a second pass over all networks and combine all non-physical networks of the same type into a single network
    combined_networks: dict[str, list[INetwork]] = defaultdict(list)
    for role, network_list in networks.items():
        # separate them by type
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

    network_repository: NetworkRepository = context.get_network_repository()
    for role, network_list in combined_networks.items():
        for network in network_list:
            network_repository.upsert(role, network)
