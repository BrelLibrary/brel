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
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.parsers.utils.optional_utils import get_or_raise
from brel.qnames.qname_utils import qname_from_str
from brel.contexts.filing_context import FilingContext
from brel.data.characteristic.characteristic_repository import CharacteristicRepository


def parse_unit_measure_from_xml(
    xml_element: _Element,  # type: ignore
    filing_context: FilingContext,
) -> QName:
    child_text = xml_element.text
    
    if child_text is None:
        error = ErrorInstance.create_error_instance(
            ErrorCode.MISSING_UNIT_MEASURE,
            xml_element
        )
        
        filing_context.get_error_repository().upsert(error)
    else:
        return qname_from_str(child_text, xml_element)


def parse_unit_from_xml(
    filing_context: FilingContext,
    xml_element: _Element,
) -> UnitCharacteristic:
    characteristic_repository: CharacteristicRepository = (
        filing_context.get_characteristic_repository()
    )
    error_repository: ErrorRepository = filing_context.get_error_repository()

    unit_id = get_str_attribute(xml_element, "id")

    if characteristic_repository.has(unit_id, UnitCharacteristic):
        error = ErrorInstance.create_error_instance(
            ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID,
            xml_element,
            id=unit_id
        )
        error_repository.upsert(error)

    numerators: list[QName] = []
    denominators: list[QName] = []

    # get the child elements of the unit and check if its tag is 'measure' or 'divide'
    children = list(xml_element)
    if len(children) != 1:
        error = ErrorInstance.create_error_instance(
            ErrorCode.XML_UNIT_ELEMENT_WITHOUT_ONE_CHILD,
            xml_element,
            id=unit_id,
            child_count=len(children)
        )

        error_repository.upsert(error)
    else:
        child = children[0]
        child_tag = child.tag
        if "measure" in child_tag:
            # get its text and parse it into a QName
            child_qname = parse_unit_measure_from_xml(child)

            numerators.append(child_qname)

        elif "divide" in child_tag:
            num_and_denom = list(child)
            if len(num_and_denom) != 2:
                error = ErrorInstance.create_error_instance(
                    ErrorCode.XML_UNIT_ELEMENT_WITHOUT_TWO_CHILDREN,
                    xml_element,
                    id=unit_id,
                    child_count=len(num_and_denom)
                )

                error_repository.upsert(error)

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
                    error = ErrorInstance.create_error_instance(
                        ErrorCode.XML_UNIT_ELEMENT_WITH_INVALID_CHILDREN,
                        xml_element,
                        id=unit_id,
                        child_tag=num_or_denom_tag
                    )

                    error_repository.upsert(error)

            if num_and_denom[0].tag == num_and_denom[1].tag:
                error = ErrorInstance.create_error_instance(
                    ErrorCode.XML_UNIT_ELEMENT_WITH_DUPLICATE_CHILDREN,
                    xml_element,
                    id=unit_id,
                    tag=num_and_denom[0].tag
                )

                error_repository.upsert(error)
        else:
            error = ErrorInstance.create_error_instance(
                ErrorCode.XML_UNIT_ELEMENT_WITH_INVALID_CHILDREN,
                xml_element,
                id=unit_id,
                child_tag=child_tag
            )

            error_repository.upsert(error)

    # create the unit characteristic, add it to the cache and return it
    unit_characteristic = UnitCharacteristic(unit_id, numerators, denominators)
    return unit_characteristic
