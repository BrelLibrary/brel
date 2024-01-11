"""
This module parses multiple etrees into a dict of networks.

@author: Robin Schmidiger
@version: 0.15
@date: 19 December 2023
"""


import lxml.etree

from brel import QName, QNameNSMap
from brel.networks import *
from brel.reportelements import *
from brel.resource import *

from typing import cast, Any
from collections import defaultdict
import json
import re
import os

from brel.parsers.XML.networks import parse_xml_link
from importlib.resources import path

# CONFIG_PATH = "brel/config/linkconfig.json"


with path("brel.config", "linkconfig.json") as config_path:
    with open(config_path, "r") as f:
        LINK_CONFIG = json.load(f)
        STANDARD_LINK_NAMES: list[str] = LINK_CONFIG["standard_link_names"]
        STANDARD_RESOURCE_ROLES: list[str] = LINK_CONFIG[
            "standard_resource_roles"
        ]
        STANDARD_LINK_ROLES: list[str] = LINK_CONFIG["standard_link_roles"]


def parse_networks_from_xmls(
    xml_trees: list[lxml.etree._ElementTree],
    qname_nsmap: QNameNSMap,
    id_to_any: dict[str, Any],
    report_elements: dict[QName, IReportElement],
) -> dict[str | None, list[INetwork]]:
    nsmap = qname_nsmap.get_nsmap()

    # first, we want to get all extended links in all xml trees
    # we do this by going over all xml trees and getting all extended links
    links = []
    for xml_tree in xml_trees:
        all_links = xml_tree.findall(
            ".//link:*[@xlink:type='extended']", namespaces=nsmap
        )
        links.extend(all_links)

    # then we want to parse the extended links with the default role first.
    # This is because some extended links may rely on labels that are defined in other extended links.
    # Specifically, the presentation networks rely on labels that are defined in the label networks.
    # Label networks have the default link role.
    def is_standard_role(role: str) -> bool:
        return any(
            map(
                lambda standard_role: standard_role is not None
                and re.match(standard_role, role),
                STANDARD_LINK_ROLES,
            )
        )

    links.sort(
        key=lambda link: is_standard_role(
            link.get("{" + nsmap["xlink"] + "}role", "")
        ),
        reverse=True,
    )

    networks: dict[str | None, list[INetwork]] = defaultdict(list)

    # go over all extended links in all xml trees
    for xml_link in links:
        # get the link role
        link_role = xml_link.get(f"{{{nsmap['xlink']}}}role", None)
        if link_role is None:
            raise ValueError(
                f"the link element {xml_link} does not have a xlink:role attribute"
            )

        # get the link name
        link_name = xml_link.tag
        if not isinstance(link_name, str):
            raise ValueError(
                f"the link element {xml_link} has an invalid tag name '{link_name}'. The tag name must be a string."
            )

        # According to the XBRL Generic Links spec, if the xlink:role is not the default link role,
        # then the ancestor linkbase must have a roleRef with the roleURI equal to the xlink:role.
        # this roleRef's href must point to a role definition that has a usedOn attribute that contains the link element's name.
        # rolerefs are only required for standard links and standard resources.
        # http://www.xbrl.org/specification/xbrl-2.1/rec-2003-12-31/xbrl-2.1-rec-2003-12-31+corrected-errata-2013-02-20.html#_3.5.2.4

        # check the integrity of all xlink:role attributes
        # If the xlink:role is NOT a standard link role and NOT a standard resource role,
        # And if the link name is a standard link name,
        # Then the ancestor linkbase needs to have a roleRef with the roleURI equal to the xlink:role.

        # Additionally, for all links read the component name from the roleRef.
        # For default links, the component name is 'None'.
        component_name = None

        link_role_elems = xml_link.findall(
            ".//*[@xlink:role]", namespaces=nsmap
        ) + [xml_link]
        for link_role_elem in link_role_elems:
            role = link_role_elem.get(f"{{{nsmap['xlink']}}}role", None)
            if role is None:
                raise ValueError(
                    f"the element {link_role_elem} does not have a xlink:role attribute"
                )
            if not isinstance(role, str):
                raise ValueError(
                    f"the element {link_role_elem} has an invalid xlink:role attribute '{role}'. The xlink:role attribute must be a string."
                )

            # check if the role is a standard role
            if any(
                map(
                    lambda standard_role: standard_role is not None
                    and re.match(standard_role, role),
                    STANDARD_LINK_ROLES,
                )
            ):
                continue

            if any(
                map(
                    lambda standard_role: standard_role is not None
                    and re.match(standard_role, role),
                    STANDARD_RESOURCE_ROLES,
                )
            ):
                continue

            # check if the link name is a standard link name
            if any(
                map(
                    lambda standard_link_name: re.match(
                        standard_link_name, link_name
                    ),
                    STANDARD_LINK_NAMES,
                )
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

                if "#" in href:
                    _, component_name = href.split("#")
                else:
                    component_name = href

        # parse the network and update the report elements
        link_networks, report_elements = parse_xml_link(
            xml_link, qname_nsmap, id_to_any, report_elements
        )

        # add the presentation network to the networks dict
        networks[component_name].extend(link_networks)

    return networks
