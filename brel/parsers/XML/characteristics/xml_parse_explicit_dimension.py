"""
Contains the xml parser for parsing an explicit dimension characteristic from an lxml.etree._Element.

:author: Robin Schmidiger
:version: 0.4
:date: 19 December 2023
"""

import lxml.etree
from typing import Callable, cast
from brel import QName
from brel.characteristics import Aspect, ICharacteristic
from brel.reportelements import Dimension, Member, IReportElement
from brel.characteristics import ExplicitDimensionCharacteristic


def parse_explicit_dimension_from_xml(
    xml_element: lxml.etree._Element,
    get_report_element: Callable[[QName], IReportElement | None],
    make_qname: Callable[[str], QName],
    get_from_cache: Callable[[str], ICharacteristic | Aspect | None],
    add_to_cache: Callable[[str, ICharacteristic | Aspect], None],
) -> ExplicitDimensionCharacteristic:
    """
    Create a Dimension from an lxml.etree._Element.
    :param xml_element: the xml subtree from which the Dimension is created
    :param get_report_element: the function to get the report element from the report elements
    :param make_qname: the function to make a QName from a string
    :param get_from_cache: the function to get a characteristic from the characteristics cache
    :param add_to_cache: the function to add a characteristic to the characteristics cache
    :returns ExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    # get the dimension attribute from the xml element
    dimension_axis = xml_element.get("dimension")
    if dimension_axis is None:
        raise ValueError(
            "Could not find dimension attribute in explicit dimension characteristic"
        )

    # check cache for dimension aspect
    dimension_aspect = get_from_cache(f"aspect {dimension_axis}")
    dimension_qname: QName = make_qname(dimension_axis)
    if dimension_aspect is None:
        dimension_aspect = Aspect.from_QName(dimension_qname)
        add_to_cache(f"aspect {dimension_axis}", dimension_aspect)
    else:
        if not isinstance(dimension_aspect, Aspect):
            raise ValueError("Dimension aspect is not a BrelAspect")
        dimension_aspect = cast(Aspect, dimension_aspect)

    # get the dimension from the report elements
    report_element = get_report_element(dimension_qname)
    if report_element is None:
        raise ValueError(
            "Dimension not found in report elements. Please make sure that the dimension is in the report elements."
        )
    if not isinstance(report_element, Dimension):
        raise ValueError(
            "Dimension not found in report elements. Please make sure that the dimension is in the report elements."
        )

    # get the dimension value from the xml element
    dimension_value = xml_element.text
    if dimension_value is None:
        raise ValueError(
            "Dimension value not found in xml element. Please make sure that the dimension value is in the xml element. {xml_dimension}"
        )
    if not isinstance(dimension_value, str):
        raise ValueError("Dimension value is not a string")

    # get the corresponding member from the report elements
    member_qname = make_qname(dimension_value)
    member = get_report_element(member_qname)
    if member is None:
        raise ValueError(
            "Member not found in report elements. Please make sure that the member is in the report elements."
        )
    if not isinstance(member, Member):
        raise ValueError(
            "Member not found in report elements. Please make sure that the member is in the report elements."
        )

    # check cache
    dimension_characteristic = get_from_cache(
        f"explicit dimension {dimension_axis} {dimension_value}"
    )
    if dimension_characteristic is None:
        # create and add the characteristic
        dimension_characteristic = ExplicitDimensionCharacteristic(
            report_element, member, dimension_aspect
        )
        add_to_cache(
            f"explicit dimension {dimension_axis} {dimension_value}",
            dimension_characteristic,
        )
    else:
        if not isinstance(
            dimension_characteristic, ExplicitDimensionCharacteristic
        ):
            raise ValueError(
                "Dimension characteristic is not an explicit dimension characteristic"
            )

    return cast(ExplicitDimensionCharacteristic, dimension_characteristic)
