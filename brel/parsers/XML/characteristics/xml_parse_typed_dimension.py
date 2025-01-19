"""
This module contains the function to parse a typed dimension from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.1
- date: 20 December 2023

====================
"""

from typing import Callable, cast

import lxml.etree

from brel import QName
from brel.characteristics import (
    Aspect,
    ICharacteristic,
    TypedDimensionCharacteristic,
)
from brel.reportelements import Dimension, IReportElement, Member


def parse_typed_dimension_from_xml(
    xml_element: lxml.etree._Element,
    get_report_element: Callable[[QName], IReportElement | None],
    make_qname: Callable[[str], QName],
    get_from_cache: Callable[[str], ICharacteristic | Aspect | None],
    add_to_cache: Callable[[str, ICharacteristic | Aspect], None],
) -> TypedDimensionCharacteristic:
    """
    Create a Dimension from an lxml.etree._Element.
    :param xml_element: the xml subtree from which the Dimension is created
    :param get_report_element: the function to get the report element from the report elements
    :param make_qname: the function to make a QName from a string
    :param get_characteristic: the function to get a characteristic from the characteristics cache
    :param add_characteristic: the function to add a characteristic to the characteristics cache
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

    # Get the dimension attribute from the xml element
    dimension_axis = xml_element.get("dimension")
    if dimension_axis is None:
        raise ValueError("Could not find dimension attribute in explicit dimension characteristic")

    # check cache for dimension aspect
    dimension_aspect = get_from_cache(f"aspect {dimension_axis}")
    dimension_qname: QName = make_qname(dimension_axis)
    if dimension_aspect is None:
        dimension_aspect = Aspect.from_QName(dimension_qname)
        add_to_cache(f"aspect {dimension_axis}", dimension_aspect)
    else:
        dimension_aspect = cast(Aspect, dimension_aspect)

    # get the report element from the report elements
    i_report_element = get_report_element(dimension_qname)
    if i_report_element is None:
        raise ValueError(
            "Dimension not found in report elements. Please make sure that the dimension is in the report elements."
        )
    if not isinstance(i_report_element, Dimension):
        raise ValueError(
            "Dimension not found in report elements. Please make sure that the dimension is in the report elements."
        )

    # get the dimension value from the xml element
    children = list(xml_element)
    if len(children) != 1:
        raise ValueError("Typed dimension characteristic has more than one child")

    value_element = children[0]
    dimension_value = value_element.text
    if dimension_value is None:
        raise ValueError(
            "Dimension value not found in xml element. Please make sure that the dimension value is in the xml element. {xml_dimension}"
        )

    # check cache
    dimension_characteristic = get_from_cache(f"typed dimension {dimension_axis} {dimension_value}")
    if dimension_characteristic is None:
        # create and add the characteristic
        dimension_characteristic = TypedDimensionCharacteristic(i_report_element, dimension_value, dimension_aspect)
        add_to_cache(
            f"typed dimension {dimension_axis} {dimension_value}",
            dimension_characteristic,
        )
    else:
        if not isinstance(dimension_characteristic, TypedDimensionCharacteristic):
            raise ValueError("Dimension characteristic is not a typed dimension characteristic")

    return cast(TypedDimensionCharacteristic, dimension_characteristic)
