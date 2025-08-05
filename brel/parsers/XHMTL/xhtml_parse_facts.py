"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""
from http.client import parse_headers
import re
import datetime

from typing import Dict, Set, cast  
from lxml.etree import _Element  # type: ignore
from lxml import etree
from brel import Context, Fact
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode
from brel.errors.error_registry import error_registry
from brel.characteristics import *
from brel.contexts.filing_context import FilingContext
from brel.errors.error_instance import ErrorInstance
from brel.parsers.XHMTL.elements.parse_continuation_chain import create_continuation_chains
from brel.parsers.XHMTL.elements.parse_header import check_no_header_element_in_head, parse_header
from brel.parsers.XHMTL.elements.parse_hidden import validate_hidden_elements
from brel.parsers.XHMTL.elements.parse_non_fraction import parse_non_fraction_fact_element
from brel.parsers.XHMTL.elements.parse_non_numeric import parse_non_numeric_fact_element
from brel.parsers.XHMTL.elements.parse_references import parse_references_elements
from brel.parsers.XHMTL.elements.parse_resources import parse_resources_elements
from brel.parsers.XHMTL.networks.xhtml_footnote_network_elements import XHTMLFootnoteNetworkElements
from brel.parsers.XML.characteristics import parse_unit_from_xml
from brel.parsers.XML.xml_context_parser import parse_context_xml
from brel.parsers.XHMTL.xhtml_parse_transformation_registry import parse_numerical_fact_value
from brel.parsers.utils.error_utils import error_on_none
from brel.parsers.utils.lxml_utils import (
    find_element,
    find_elements,
    get_prefix_localname_tag,
    get_str_attribute,
    get_str_attribute_optional,
)
from brel.parsers.utils.optional_utils import get_or_raise
from urllib.parse import urlparse

def parse_headers(etrees: list[_Element], error_repository: ErrorRepository) -> None:    
    has_headers = False

    hidden_elements, resources_elements, references_elements = [], [], []
    for xbrl_instance in etrees:
        check_no_header_element_in_head(xbrl_instance, error_repository)
        headers = find_elements(xbrl_instance, './/ix:header')
        if not headers:
            continue
    
        has_headers = True
        for header in headers:
            hidden, resources, references = parse_header(header, error_repository)
            hidden_elements += hidden
            resources_elements += resources
            references_elements += references
    
    if not has_headers:
        error = ErrorInstance.create_error_instance(ErrorCode.IXBRL_NO_HEADER_ELEMENTS)
        error_repository.upsert(error)

    if not resources_elements:
        error = ErrorInstance.create_error_instance(ErrorCode.IXBRL_NO_RESOURCES_ELEMENT)
        error_repository.upsert(error)
    
    return hidden_elements, resources_elements, references_elements

def parse_contexts(context_elements: list[_Element], filing_context: FilingContext, taken_ids: Set[str]) -> None:
    context_repository = filing_context.get_context_repository()
    error_repository = filing_context.get_error_repository()

    for context_element in context_elements:
        id = get_str_attribute_optional(context_element, 'id')

        if id is None:
            error = ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_CONTEXT_WITHOUT_ID,
                context_element
            )

            error_repository.upsert(error)        
    
        if id in taken_ids:
            error = ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID,
                context_element,
                id=id
            )
            error_repository.upsert(error)
            
        taken_ids.add(id)
        
        context = parse_context_xml(filing_context, context_element, [])
        context_repository.add_context(context)

def parse_units(unit_elements: list[_Element], filing_context: FilingContext, taken_ids: Set[str]) -> None:
    characteristic_repository = filing_context.get_characteristic_repository()
    
    for unit_element in unit_elements:
        id = get_str_attribute_optional(unit_element, 'id')

        if id is None:
            error = ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_UNIT_WITHOUT_ID,
                unit_element
            )

            filing_context.get_error_repository().upsert(error)

        if id in taken_ids:
            error = ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID,
                unit_element,
                id=id
            )

            filing_context.get_error_repository().upsert(error)
        
        taken_ids.add(id)

        unit = parse_unit_from_xml(filing_context, unit_element)
        characteristic_repository.upsert(unit.get_id(), unit)

def parse_instance_elements(etrees: list[_Element]) -> None:
    fact_elements, footnote_elements, continuation_elements = [], [], []
    for xbrl_instance in etrees:
        facts = find_elements(xbrl_instance, ".//ix:nonNumeric | .//ix:nonFraction")
        footnotes = find_elements(xbrl_instance, ".//ix:footnote")
        continuations = find_elements(xbrl_instance, ".//ix:continuation")

        fact_elements += facts
        footnote_elements += footnotes
        continuation_elements += continuations

    return fact_elements, footnote_elements, continuation_elements

def parse_facts(fact_elements: list[_Element], continuation_chains: Dict[_Element, list[_Element]], filing_context: FilingContext, taken_ids: Set[str]) -> None:
    report_element_repository = filing_context.get_report_element_repository()
    context_repository = filing_context.get_context_repository()
    characteristics_repository = filing_context.get_characteristic_repository()
    fact_repository = filing_context.get_fact_repository()
    error_repository = filing_context.get_error_repository()

    for fact_element in fact_elements:
        element_tag = get_prefix_localname_tag(fact_element.tag)
        characteristics: list[UnitCharacteristic | ConceptCharacteristic] = []

        concept_name = get_str_attribute_optional(fact_element, "name")
        if concept_name is None:
            error = ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_FACT_WITHOUT_CONCEPT_NAME,
                fact_element,
                fact_id=get_str_attribute_optional(fact_element, "id")
            )
            error_repository.upsert(error)

        concept_characteristic = report_element_repository.get(concept_name, ConceptCharacteristic)
        characteristics.append(concept_characteristic)

        unit_id = get_str_attribute_optional(fact_element, "unitRef")

        if unit_id:
            unit_characteristic = characteristics_repository.get(unit_id, UnitCharacteristic)
            characteristics.append(unit_characteristic)
        elif not unit_id and element_tag == 'ix:nonFraction':
            raise ValueError(f"The numeric fact {fact_element.get('id')} needs to have a unitRef attribute")

        context_id = get_str_attribute_optional(fact_element, "contextRef")

        if context_id is None:
            error = ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_FACT_WITHOUT_CONTEXT,
                fact_element,
                fact_id=get_str_attribute_optional(fact_element, "id")
            )

            error_repository.upsert(error)

        context = context_repository.get_context_copy(context_id)

        for characteristic in characteristics:
            context._add_characteristic(characteristic)
        
        if element_tag == 'ix:nonNumeric':
            continuation_chain = continuation_chains.get(fact_element)
            fact = parse_non_numeric_fact_element(fact_element, context, continuation_chain, taken_ids)
        elif element_tag == 'ix:nonFraction':
            fact = parse_non_fraction_fact_element(fact_element, context, taken_ids)

        fact_repository.upsert(fact)

def parse_facts_xhtml(filing_context: FilingContext) -> None:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    """
    xml_service = filing_context.get_xml_service()

    etrees = list(filter(
        lambda x: not x.tag.endswith('schema') and not x.tag.endswith('linkbase'),
        xml_service.get_all_etrees()
    ))

    hidden_elements, resources_elements, references_elements = parse_headers(etrees, filing_context)

    taken_ids: Set[str] = set()
    parse_references_elements(references_elements, taken_ids, filing_context)

    relationship_elements, role_ref_elements, arcrole_ref_elements, context_elements, unit_elements =\
        parse_resources_elements(resources_elements, filing_context)
    
    parse_contexts(context_elements, filing_context, taken_ids)
    parse_units(unit_elements, filing_context, taken_ids)
    validate_hidden_elements(hidden_elements, taken_ids)

    fact_elements, footnote_elements, continuation_elements = parse_instance_elements(etrees)
    continuation_chains = create_continuation_chains(fact_elements, footnote_elements, continuation_elements, taken_ids)
    parse_facts(fact_elements, continuation_chains, filing_context, taken_ids)

    return XHTMLFootnoteNetworkElements(
        footnote_elements,
        continuation_chains,
        relationship_elements,
        role_ref_elements,
        arcrole_ref_elements,
        taken_ids
    )

if __name__ == "__main__":
    data = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">1 <b> <d> b </d> </b> 2 <c> c </c> 4 </xs:schema>'
    root = etree.fromstring(data)
    root.insert()
    root.remove(root[1])
    print(etree.tostring(root))
