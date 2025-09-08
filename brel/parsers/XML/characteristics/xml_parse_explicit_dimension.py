"""
Contains the xml parser for parsing an explicit dimension characteristic from an lxml.etree._Element.

====================

:author: Robin Schmidiger
:version: 0.5
:date: 13 April 2025

====================
"""

from typing import Optional
import lxml.etree

from brel.characteristics import (
    Aspect,
    ExplicitDimensionCharacteristic,
)
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qnames.qname_utils import qname_from_str
from brel.reportelements import Dimension, Member
from brel.contexts.filing_context import FilingContext
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.data.characteristic.characteristic_repository import CharacteristicRepository
from brel.parsers.utils.error_utils import error_on_none


def parse_explicit_dimension_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
) -> Optional[ExplicitDimensionCharacteristic]:
    """
    Create a Dimension from an lxml.etree._Element, return it and add it to the characteristic repository.
    :param xml_element: the xml subtree from which the Dimension is created
    :returns ExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element or
    None if the dimension _Element is malformed
    """
    report_element_repository: ReportElementRepository = (
        filing_context.get_report_element_repository()
    )
    characteristic_repository: CharacteristicRepository = (
        filing_context.get_characteristic_repository()
    )
    aspect_repository = filing_context.get_aspect_repository()
    error_repository = filing_context.get_error_repository()

    aspect_id = get_str_attribute(xml_element, "dimension")
    if not characteristic_repository.has(aspect_id, ExplicitDimensionCharacteristic):
        aspect_repository.upsert(Aspect(aspect_id, []))

    aspect = aspect_repository.get(aspect_id)

    member_id = error_on_none(
        xml_element.text, f"Dimension value not found in xml element {xml_element}"
    )

    dimension_qname = qname_from_str(aspect_id, xml_element)
    if not report_element_repository.has_typed_qname(dimension_qname, Dimension):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.INVALID_DIMENSION_ATTRIBUTE_VALUE,
                xml_element,
                dimension=aspect_id,
            )
        )
        return None

    dimension = report_element_repository.get_typed_by_qname(dimension_qname, Dimension)

    member_qname = qname_from_str(member_id, xml_element)
    if not report_element_repository.has_typed_qname(member_qname, Member):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.INVALID_DIMENSION_MEMBER,
                xml_element,
                member=member_id,
                dimension=aspect_id,
            )
        )
        return None

    member = report_element_repository.get_typed_by_qname(member_qname, Member)

    dimension_id = f"{aspect_id} {member_id}"
    if not characteristic_repository.has(dimension_id, ExplicitDimensionCharacteristic):
        characteristic_repository.upsert(
            dimension_id,
            ExplicitDimensionCharacteristic(dimension, member, aspect),
        )

    return characteristic_repository.get(dimension_id, ExplicitDimensionCharacteristic)
