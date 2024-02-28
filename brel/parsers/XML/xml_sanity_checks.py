"""
Adds some sanity checks for the XML files.
These are checks that are not covered by the XML schema.
They are in line with the checks that the SEC EDGAR renderer does.
The list of checks is not exhaustive.
It includes the following checks:
- check for duplicate rolerefs in linkbases and the instance document
- check if all rolerefs point to a existing role

====================

- author: Robin Schmidiger
- version: 0.15
- date: 04 January 2024

====================
"""

from typing import TypeGuard

import lxml.etree

from brel import QNameNSMap
from brel.parsers.dts import XMLFileManager


def check_duplicate_rolerefs(
    file_manager: XMLFileManager,
    qname_nsmap: QNameNSMap,
) -> None:
    """
    Checks for duplicate rolerefs in linkbases and the instance document.
    Duplicate rolerefs are rolerefs with the same roleURI.
    Duplicate rolerefs are not allowed according to the XBRL specification.
    :param file_manager: the file manager that contains the instance document and all linkbases
    :param qname_nsmap: the QNameNSMap
    :return: None
    :raises ValueError: if there are duplicate rolerefs
    """

    nsmap = qname_nsmap.get_nsmap()

    xml_trees = file_manager.get_all_files()

    # check for duplicate rolerefs
    # find all rolerefs and put their parents into a set
    roleref_parents: set[lxml.etree._Element] = set()
    for xml_tree in xml_trees:
        rolerefs = xml_tree.findall(".//link:roleRef", namespaces=nsmap)

        def get_parent(
            roleref: lxml.etree._Element,
        ) -> lxml.etree._Element | None:
            return roleref.getparent()

        def filter_none(
            roleref_parent: lxml.etree._Element | None,
        ) -> TypeGuard[lxml.etree._Element]:
            return roleref_parent is not None

        roleref_parents.update(
            filter(
                filter_none,
                map(get_parent, rolerefs),
            )
        )

    # for each parent, get all roleref children and check if there are duplicates
    for roleref_parent in roleref_parents:
        rolerefs = roleref_parent.findall(".//link:roleRef", namespaces=nsmap)
        roleURIs = list(map(lambda roleref: roleref.get("roleURI"), rolerefs))
        if len(roleURIs) != len(set(roleURIs)):
            raise ValueError(
                f"the linkbase {roleref_parent} has duplicate rolerefs. All rolerefs must have a unique roleURI attribute."
            )


def check_duplicate_arcs(
    file_manager: XMLFileManager,
    qname_nsmap: QNameNSMap,
) -> None:
    """
    Checks for duplicate arcs in linkbases.
    Duplicate arcs are arcs with the same from and to attributes.
    Duplicate arcs are not allowed according to the XBRL specification.
    :param file_manager: the file manager that contains the instance document and all linkbases
    :param qname_nsmap: the QNameNSMap
    :return: None
    :raises ValueError: if there are duplicate arcs
    """

    nsmap = qname_nsmap.get_nsmap()

    xml_trees = file_manager.get_all_files()

    # check for duplicate arcs
    # find all elements with an @xlink:type='extended' attribute and put their parents into a set
    extended_links: set[lxml.etree._Element] = set()
    for xml_tree in xml_trees:
        extended_links.update(xml_tree.findall(".//*[@xlink:type='extended']", namespaces=nsmap))

    # for each link, get all arcs and check if there are duplicates
    for extended_link in extended_links:
        arcs = extended_link.findall(".//link:arc", namespaces=nsmap)
        arc_from_to = list(map(lambda arc: (arc.get("from"), arc.get("to")), arcs))
        if len(arc_from_to) != len(set(arc_from_to)):
            raise ValueError(
                f"the link {extended_link} has duplicate arcs. All arcs must have a unique from and to attribute."
            )
