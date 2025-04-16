"""
This module contains the function to parse the contexts from the xbrl instance.
It parses XBRL in the XML syntax.
It only parses the syntactic context, therefore the Unit and Concept characteristics are not parsed and must be provided as arguments.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 April 2025

====================
"""


import lxml.etree

from brel import Context
from brel.characteristics import *
from brel.parsers.XML.characteristics import *
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.reportelements import *
from brel.contexts.filing_context import FilingContext
from brel.parsers.utils.error_utils import error_on_none


def parse_context_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
    characteristics: list[UnitCharacteristic | ConceptCharacteristic],
) -> "Context":
    """
    Creates a Context from an lxml.etree._Element.
    :param xml_element: lxml.etree._Element. The lxml.etree._Element to create the Context from.
    :param characteristics: list[ICharacteristic]. The characteristics to use for the context. If the context contains a dimension, then both the dimension and the member must be in the characteristics.
    :param report_elements: list[IReportElement]. The report elements to use for the context. If the context contains a dimension, then both the dimension and the member must be in the report elements.
    :param qname_nsmap: QNameNSMap. The QNameNSMap to use for the context.
    :param characteristics_cache: dict[str, ICharacteristic]. The characteristics cache to use for the context.
    :returns Context: The context created from the lxml.etree._Element.
    :raises ValueError: if the XML element is malformed
    """

    context_id = get_str_attribute(xml_element, "id")

    context_period = error_on_none(
        xml_element.find("{*}period", namespaces=None),
        f"Could not find period element in {xml_element}",
    )

    context_entity = error_on_none(
        xml_element.find("{*}entity", namespaces=None),
        f"Could not find entity element in {xml_element}",
    )

    fact_context = Context(context_id)

    # add the characteristics provided by the user. these are the unit and concept
    for characteristic in characteristics:
        fact_context._add_characteristic(characteristic)

    fact_context._add_characteristic(
        parse_period_from_xml(filing_context, context_period)
    )
    fact_context._add_characteristic(
        parse_entity_from_xml(filing_context, context_entity)
    )

    # add the dimensions. the dimensions are the children of context/entity/segment
    segment = context_entity.find("{*}segment", namespaces=None)

    if segment is not None:
        for xml_dimension in segment:
            if "explicitMember" in xml_dimension.tag:
                explicit_dimension_characteristic = parse_explicit_dimension_from_xml(
                    filing_context, xml_dimension
                )
                fact_context._add_characteristic(explicit_dimension_characteristic)
            elif "typedMember" in xml_dimension.tag:
                typed_dimension_characteristic = parse_typed_dimension_from_xml(
                    filing_context, xml_dimension
                )
                fact_context._add_characteristic(typed_dimension_characteristic)
            else:
                raise ValueError(
                    f"Unknown dimension type {xml_dimension.tag}. Please make sure that the dimension is either an explicitMember or a typedMember. {xml_dimension.tag}"
                )

    return fact_context
