"""
This module contains the function to parse the contexts from the xbrl instance.
It parses XBRL in the XML syntax.
It only parses the syntactic context, therefore the Unit and Concept characteristics are not parsed and must be provided as arguments.

@author: Robin Schmidiger
@version: 0.1
@date: 19 December 2023
"""

import lxml.etree
from brel import QName, Context
from brel.characteristics import *
from brel.reportelements import *
from brel.parsers.XML.characteristics import *

from typing import cast, Callable


def parse_context_xml(
    xml_element: lxml.etree._Element,
    characteristics: list[UnitCharacteristic | ConceptCharacteristic],
    make_qname: Callable[[str], QName],
    get_report_element: Callable[[QName], IReportElement | None],
    get_from_cache: Callable[[str], ICharacteristic | Aspect | None],
    add_to_cache: Callable[[str, ICharacteristic | Aspect], None],
) -> "Context":
    """
    Creates a Context from an lxml.etree._Element.
    :param xml_element: lxml.etree._Element. The lxml.etree._Element to create the Context from.
    :param characteristics: list[ICharacteristic]. The characteristics to use for the context. If the context contains a dimension, then both the dimension and the member must be in the characteristics.
    :param report_elements: list[IReportElement]. The report elements to use for the context. If the context contains a dimension, then both the dimension and the member must be in the report elements.
    :param qname_nsmap: QNameNSMap. The QNameNSMap to use for the context.
    :param characteristics_cache: dict[str, ICharacteristic]. The characteristics cache to use for the context.
    :returns: Context. The context created from the lxml.etree._Element.
    :raises ValueError: if the XML element is malformed
    """

    context_id = xml_element.get("id")
    if context_id is None:
        raise ValueError("Could not find id attribute in context")

    # check if the supplied list of characteristics only contains units and concepts
    for characteristic in characteristics:
        if not isinstance(
            characteristic, UnitCharacteristic
        ) and not isinstance(characteristic, ConceptCharacteristic):
            raise ValueError(
                f"Context id {context_id} contains a characteristic that is not a unit or a concept. Please make sure that the list of characteristics only contains units and concepts."
            )

    context_period = xml_element.find("{*}period", namespaces=None)
    context_entity = xml_element.find("{*}entity", namespaces=None)

    if context_period is None:
        raise ValueError(
            f"Context id {context_id!r} does not contain a period. Please make sure that the context contains a period."
        )

    if context_entity is None:
        raise ValueError(
            f"Context id {context_id!r} does not contain an entity. Please make sure that the context contains an entity."
        )

    context = Context(context_id)

    # add the characteristics provided by the user. these are the unit and concept
    for characteristic in characteristics:
        context._add_characteristic(characteristic)

    context._add_characteristic(
        parse_period_from_xml(context_period, get_from_cache, add_to_cache)
    )
    context._add_characteristic(
        parse_entity_from_xml(context_entity, get_from_cache, add_to_cache)
    )

    # add the dimensions. the dimensions are the children of context/entity/segment
    segment = context_entity.find("{*}segment", namespaces=None)

    if segment is not None:
        for xml_dimension in segment:
            # if it is an explicit dimension, the tag is xbrli:explicitMember
            if "explicitMember" in xml_dimension.tag:
                explicit_dimension_characteristic = (
                    parse_explicit_dimension_from_xml(
                        xml_dimension,
                        get_report_element,
                        make_qname,
                        get_from_cache,
                        add_to_cache,
                    )
                )
                context._add_characteristic(explicit_dimension_characteristic)
            # if it is a typed dimension, the tag is xbrli:typedMember
            elif "typedMember" in xml_dimension.tag:
                typed_dimension_characteristic = (
                    parse_typed_dimension_from_xml(
                        xml_dimension,
                        get_report_element,
                        make_qname,
                        get_from_cache,
                        add_to_cache,
                    )
                )
                context._add_characteristic(typed_dimension_characteristic)

            else:
                raise ValueError(
                    f"Unknown dimension type {xml_dimension.tag}. Please make sure that the dimension is either an explicitMember or a typedMember. {xml_dimension.tag}"
                )

    return context
