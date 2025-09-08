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


from typing import Optional
import lxml.etree

from brel import Context
from brel.characteristics import *
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.parsers.XML.characteristics import *
from brel.parsers.utils.lxml_utils import get_str_attribute
from brel.reportelements import *
from brel.contexts.filing_context import FilingContext
from brel.parsers.utils.error_utils import error_on_none


def parse_context_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
    characteristics: list[UnitCharacteristic | ConceptCharacteristic],
) -> Optional[Context]:
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

    context_period = xml_element.find("{*}period", namespaces=None)

    if context_period is None:
        error = ErrorInstance.create_error_instance(
            ErrorCode.MISSING_CONTEXT_PERIOD, xml_element
        )
        filing_context.get_error_repository().upsert(error)
        return None

    context_entity = xml_element.find("{*}entity", namespaces=None)
    if context_entity is None:
        error = ErrorInstance.create_error_instance(
            ErrorCode.MISSING_CONTEXT_ENTITY, xml_element
        )
        filing_context.get_error_repository().upsert(error)
        return None

    fact_context = Context(context_id)

    # add the characteristics provided by the user. these are the unit and concept
    for characteristic in characteristics:
        fact_context._add_characteristic(characteristic)

    period = parse_period_from_xml(filing_context, context_period)
    if period is not None:
        fact_context._add_characteristic(period)

    entity = parse_entity_from_xml(filing_context, context_entity)
    if entity is not None:
        fact_context._add_characteristic(entity)

    # add the dimensions. the dimensions are the children of context/entity/segment
    segment = context_entity.find("{*}segment", namespaces=None)

    if segment is not None:
        for xml_dimension in segment:
            if "explicitMember" in xml_dimension.tag:
                explicit_dimension_characteristic = parse_explicit_dimension_from_xml(
                    filing_context, xml_dimension
                )

                if explicit_dimension_characteristic is None:
                    continue

                fact_context._add_characteristic(explicit_dimension_characteristic)
            elif "typedMember" in xml_dimension.tag:
                typed_dimension_characteristic = parse_typed_dimension_from_xml(
                    filing_context, xml_dimension
                )
                fact_context._add_characteristic(typed_dimension_characteristic)
            else:
                error = ErrorInstance.create_error_instance(
                    ErrorCode.INVALID_DIMENSION_TYPE, xml_dimension
                )

                filing_context.get_error_repository().upsert(error)

    return fact_context
