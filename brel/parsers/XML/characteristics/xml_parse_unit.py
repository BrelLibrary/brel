"""
This module contains the function for parsing an xml subtree into a Unit characteristic.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 12 May 2025

====================
"""


from lxml.etree import _Element  # type: ignore

from brel import QName
from brel.characteristics import UnitCharacteristic
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.parsers.utils.optional_utils import get_or_raise
from brel.qnames.qname_utils import qname_from_str
from brel.contexts.filing_context import FilingContext
from brel.data.characteristic.characteristic_repository import CharacteristicRepository


def parse_unit_measure_from_xml(
    xml_element: _Element,  # type: ignore
) -> QName:
    child_text = get_or_raise(
        xml_element.text, ValueError(f"The measure {xml_element} has no text")
    )
    return qname_from_str(child_text, xml_element)


def parse_unit_from_xml(
    filing_context: FilingContext,
    xml_element: _Element,
) -> UnitCharacteristic:
    characteristic_repository: CharacteristicRepository = (
        filing_context.get_characteristic_repository()
    )

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
        child_qname = parse_unit_measure_from_xml(child)

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
                child_qname = parse_unit_measure_from_xml(num_or_denom)

                numerators.append(child_qname)
            elif "unitDenominator" in num_or_denom_tag:
                # get its text and parse it into a QName
                child_qname = parse_unit_measure_from_xml(num_or_denom)

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
