"""
This module contains the function to parse a typed dimension from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 April 2025

====================
"""


import lxml.etree

from brel.characteristics import (
    Aspect,
    TypedDimensionCharacteristic,
)
from brel.contexts.filing_context import FilingContext
from brel.parsers.utils.iterable_utils import get_first
from brel.parsers.utils.error_utils import error_on_none
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.qname import QName
from brel.reportelements import Dimension


def parse_typed_dimension_from_xml(
    filing_context: FilingContext, xml_element: lxml.etree._Element  # type: ignore
) -> TypedDimensionCharacteristic:
    """
    Create a Dimension from an lxml.etree._Element.
    :param xml_element: the xml subtree from which the Dimension is created
    :returns ExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """

    """
    A typed dimension may look like this:
    <xbrli:typedMember dimension="us-gaap:StatementClassOfStockAxis">
        <us-gaap:StatementClassOfStockAxis.domain>us-gaap:ClassACommonStockMember</us-gaap:StatementClassOfStockAxis.domain>
    </xbrli:typedMember>
    
    The three relevant parts are:
    - the tag (xbrli:typedMember)
    - the dimension attribute, "us-gaap:StatementClassOfStockAxis" in this case
    - the value of the domain element, "us-gaap:ClassACommonStockMember" in this case
    Note that the tag us-gaap:StatementClassOfStockAxis.domain is just a dummy tag and is not used.

    From xbrli:typedMember, we know that we are dealing with a typed dimension.
    From the dimension attribute, we know which dimension we are dealing with.
    From the value of the domain element, we know which member we are dealing with.
    """
    aspect_repository = filing_context.get_aspect_repository()
    report_element_repository = filing_context.get_report_element_repository()
    characteristic_repository = filing_context.get_characteristic_repository()
    nsmap = filing_context.get_nsmap()

    dimension_axis = get_str_attribute(xml_element, "dimension")

    if not aspect_repository.has(dimension_axis):
        aspect_repository.upsert(Aspect.from_str(dimension_axis))
    dimension_aspect = aspect_repository.get(dimension_axis)

    i_report_element = report_element_repository.get_typed_by_qname(
        QName.from_string(dimension_axis, nsmap), Dimension
    )

    value_element = get_first(
        xml_element, "Typed dimension characteristic has more than one child"
    )
    dimension_value = error_on_none(
        value_element.text,
        f"Dimension value not found in xml element. Please make sure that the dimension value is in the xml element. {xml_element}",
    )

    dimension_id = f"{dimension_axis} {dimension_value}"
    if not characteristic_repository.has(dimension_id, TypedDimensionCharacteristic):
        dimension_characteristic = TypedDimensionCharacteristic(
            i_report_element, dimension_value, dimension_aspect
        )
        characteristic_repository.upsert(dimension_id, dimension_characteristic)

    return characteristic_repository.get(dimension_id, TypedDimensionCharacteristic)
