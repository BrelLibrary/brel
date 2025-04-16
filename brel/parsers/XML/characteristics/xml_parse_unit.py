"""
This module contains the function for parsing an xml subtree into a Unit characteristic.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 13 April 2025

====================
"""

from typing import Callable

import lxml.etree

from brel import QName
from brel.characteristics import UnitCharacteristic
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.reportelements import Concept
from brel.contexts.filing_context import FilingContext
from brel.data.characteristic.characteristic_repository import CharacteristicRepository


def parse_unit_measure_from_xml(
    xml_element: lxml.etree._Element,  # type: ignore
    concept: Concept,
    make_qname: Callable[[str], QName],
) -> QName:
    """
    Create a Unit measure from an xml subtree.
    :param xml_element: the xml subtree from which the Unit measure is created
    :param concept: the concept of the unit. What units are allowed is defined by the concept.
    :param make_qname: the function to make a QName from a string
    """
    child_text = xml_element.text
    if child_text is None:
        raise ValueError(f"The measure {xml_element} has no text")
    if ":" not in child_text:
        child_text = f"xbrli:{child_text}"
    child_qname = make_qname(child_text)

    # get the type of the concept
    concept_type = concept.get_data_type()

    # according to the xbrl spec, if the concept type is 'monetaryItemType', the unit must be a ISO 4217 currency designation
    child_localname = child_qname.get_local_name()
    if concept_type == "monetaryItemType" and (
        "4217" not in child_localname or "ISO" not in child_localname.upper()
    ):
        raise ValueError(
            f"The measure {child_qname} is not an ISO 4217 currency designation"
        )

    # according to the xbrl spec, if the concept type is 'sharesItemType', the unit must be the qname xbrli:shares
    if concept_type == "sharesItemType" and child_qname != make_qname("xbrli:shares"):
        raise ValueError(f"The measure {child_qname} is not xbrli:shares")

    return child_qname


def parse_unit_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
    concept: Concept,
) -> UnitCharacteristic:
    """
    Create a Unit from an xml subtree.
    :param xml_element: the xml subtree from which the Unit is created
    :param concept: the concept of the unit. What units are allowed is defined by the concept.
    :param make_qname: the function to make a QName from a string
    :param get_characteristic: the function to get a characteristic from the characteristics cache
    :param add_characteristic: the function to add a characteristic to the characteristics cache
    """
    characteristic_repository: CharacteristicRepository = (
        filing_context.get_characteristic_repository()
    )

    def make_qname(name: str) -> QName:
        return QName.from_string(name, filing_context.get_nsmap())

    unit_id = get_str_attribute(xml_element, "id")

    if characteristic_repository.has(unit_id, UnitCharacteristic):
        return characteristic_repository.get(unit_id, UnitCharacteristic)

    numerators: list[QName] = []
    denominators: list[QName] = []

    # get the child elements of the unit and check if its tag is 'measure' or 'divide'
    children = list(xml_element)
    if len(children) != 1:
        raise ValueError(
            f"The unit {unit_id} has {len(children)} children but should have 1 child"
        )

    child = children[0]
    child_tag = child.tag
    if "measure" in child_tag:
        # get its text and parse it into a QName
        child_qname = parse_unit_measure_from_xml(child, concept, make_qname)

        numerators.append(child_qname)

    elif "divide" in child_tag:
        num_and_denom = list(child)
        if len(num_and_denom) != 2:
            raise ValueError(
                f"The unit {unit_id} has {len(num_and_denom)} children but should have 2 children"
            )

        for num_or_denom in num_and_denom:
            num_or_denom_tag = num_or_denom.tag
            if "unitNumerator" in num_or_denom_tag:
                # get its text and parse it into a QName
                child_qname = parse_unit_measure_from_xml(
                    num_or_denom, concept, make_qname
                )

                numerators.append(child_qname)
            elif "unitDenominator" in num_or_denom_tag:
                # get its text and parse it into a QName
                child_qname = parse_unit_measure_from_xml(
                    num_or_denom, concept, make_qname
                )

                denominators.append(child_qname)
            else:
                raise ValueError(
                    f"The unit {unit_id} has child {num_or_denom_tag} but should have children 'unitNumerator' and 'unitDenominator'"
                )

        if num_and_denom[0].tag == num_and_denom[1].tag:
            raise ValueError(
                f"The unit {unit_id} has two children with the same tag: {num_and_denom[0].tag}. One should be 'unitNumerator' and the other 'unitDenominator'"
            )
    else:
        raise ValueError(
            f"The unit {unit_id} has child {child_tag} but should have child 'measure' or 'divide'"
        )

    # create the unit characteristic, add it to the cache and return it
    unit_characteristic = UnitCharacteristic(unit_id, numerators, denominators)
    characteristic_repository.upsert(unit_id, unit_characteristic)
    return unit_characteristic
