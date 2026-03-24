"""
This module contains the function for parsing an xml subtree into a Unit characteristic.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 12 May 2025

====================
"""

from typing import Optional
from lxml.etree import _Element  # type: ignore

from brel import QName
from brel.characteristics import UnitCharacteristic
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode

from brel.parsers.utils.lxml_utils import get_str_attribute, get_str_attribute_optional
from brel.qnames.qname_utils import qname_from_str
from brel.contexts.filing_context import FilingContext
from brel.data.characteristic.characteristic_repository import CharacteristicRepository


def parse_unit_measure_from_xml(
    xml_element: _Element,  # type: ignore
    filing_context: FilingContext,
) -> Optional[QName]:
    child_text = xml_element.text
    error_repository = filing_context.get_error_repository()
    if child_text is None:
        error_repository.insert(ErrorCode.XML_MISSING_UNIT_MEASURE, xml_element)
        return None
    else:
        qname = qname_from_str(child_text, xml_element)
        return qname

        # if isinstance(qname_or_error, ErrorInstance):
        #     error_repository.insert(qname_or_error)
        #     return None

        # return qname_or_error


def parse_unit_from_xml(
    filing_context: FilingContext,
    xml_element: _Element,
) -> Optional[UnitCharacteristic]:
    characteristic_repository: CharacteristicRepository = (
        filing_context.get_characteristic_repository()
    )
    error_repository: ErrorRepository = filing_context.get_error_repository()

    unit_id = get_str_attribute(xml_element, "id")

    if characteristic_repository.has(unit_id, UnitCharacteristic):
        error_repository.insert(
            ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, xml_element, id=unit_id
        )

    numerators: list[QName] = []
    denominators: list[QName] = []

    # get the child elements of the unit and check if its tag is 'measure' or 'divide'
    children = list(xml_element)
    if len(children) != 1:
        error_repository.insert(
            ErrorCode.XML_UNIT_ELEMENT_WITHOUT_ONE_CHILD,
            xml_element,
            id=unit_id,
            child_count=str(len(children)),
        )
    else:
        child = children[0]
        child_tag = child.tag
        if "measure" in child_tag:
            # get its text and parse it into a QName
            child_qname = parse_unit_measure_from_xml(child, filing_context)
            if not child_qname:
                return None

            numerators.append(child_qname)

        elif "divide" in child_tag:
            num_and_denom = list(child)
            if len(num_and_denom) != 2:
                error_repository.insert(
                    ErrorCode.XML_DIVIDE_ELEMENT_WITHOUT_TWO_CHILDREN,
                    xml_element,
                    id=unit_id,
                    child_count=str(len(num_and_denom)),
                )

            for num_or_denom in num_and_denom:
                num_or_denom_tag = num_or_denom.tag

                if (
                    "unitNumerator" not in num_or_denom_tag
                    and "unitDenominator" not in num_or_denom_tag
                ):
                    error_repository.insert(
                        ErrorCode.XML_INVALID_DIVIDE_ELEMENT_CHILDREN,
                        xml_element,
                        id=unit_id,
                        child_tag=num_or_denom_tag,
                    )

                measure_child = num_or_denom[0]
                child_qname = parse_unit_measure_from_xml(measure_child, filing_context)

                if not child_qname:
                    return None

                if "unitNumerator" in num_or_denom_tag:
                    numerators.append(child_qname)
                elif "unitDenominator" in num_or_denom_tag:
                    denominators.append(child_qname)

            if num_and_denom[0].tag == num_and_denom[1].tag:
                error_repository.insert(
                    ErrorCode.XML_DUPLICATE_DIVIDE_ELEMENT_CHILDREN,
                    xml_element,
                    id=unit_id,
                    tag=num_and_denom[0].tag,
                )
        else:
            error_repository.insert(
                ErrorCode.XML_INVALID_UNIT_ELEMENT_CHILDREN,
                xml_element,
                id=unit_id,
                child_tag=child_tag,
            )

    # create the unit characteristic, add it to the cache and return it
    unit_characteristic = UnitCharacteristic(unit_id, numerators, denominators)
    return unit_characteristic
