"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""
import re
import datetime

from typing import Dict, List, Set, Tuple, cast
from lxml.etree import _Element, _ElementTree  # type: ignore
from lxml import etree
from brel import Context, Fact
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode
from brel.characteristics import *
from brel.contexts.filing_context import FilingContext

from brel.parsers.XHMTL.elements.parse_continuation_chain import (
    create_continuation_chains,
)
from brel.parsers.XHMTL.elements.parse_header import (
    check_no_header_element_in_head,
    parse_header,
)
from brel.parsers.XHMTL.elements.parse_hidden import validate_hidden_elements
from brel.parsers.XHMTL.elements.parse_non_fraction import (
    parse_non_fraction_fact_element,
)
from brel.parsers.XHMTL.elements.parse_non_numeric import parse_non_numeric_fact_element
from brel.parsers.XHMTL.elements.parse_references import parse_references_elements
from brel.parsers.XHMTL.elements.parse_resources import parse_resources_elements
from brel.parsers.XHMTL.networks.xhtml_footnote_network_elements import (
    XHTMLFootnoteNetworkElements,
)
from brel.parsers.XML.characteristics import parse_unit_from_xml
from brel.parsers.XML.xml_context_parser import parse_context_xml
from brel.parsers.utils.lxml_utils import (
    find_elements,
    get_prefix_localname_tag,
    get_str_attribute_optional,
)

from brel.qnames.qname_utils import qname_from_str
from brel.reportelements.concept import Concept


def parse_headers(
    etrees: list[_Element], error_repository: ErrorRepository
) -> Tuple[List[_Element], List[_Element], List[_Element]]:
    has_headers = False

    hidden_elements, resources_elements, references_elements = [], [], []
    for xbrl_instance in etrees:
        check_no_header_element_in_head(xbrl_instance, error_repository)
        headers = find_elements(
            xbrl_instance,
            ".//ix:header",
            namespaces={"ix": "http://www.xbrl.org/2013/inlineXBRL"},
        )
        if len(headers) == 0:
            continue

        has_headers = True
        for header in headers:
            hidden, resources, references = parse_header(header, error_repository)
            hidden_elements += hidden
            resources_elements += resources
            references_elements += references

    if not has_headers:
        error_repository.insert(ErrorCode.IXBRL_NO_HEADER_ELEMENTS)

    if not resources_elements:
        error_repository.insert(ErrorCode.IXBRL_NO_RESOURCES_ELEMENTS)

    return hidden_elements, resources_elements, references_elements


def parse_contexts(
    context_elements: list[_Element], filing_context: FilingContext, taken_ids: Set[str]
) -> None:
    context_repository = filing_context.get_context_repository()
    error_repository = filing_context.get_error_repository()

    for context_element in context_elements:
        id = get_str_attribute_optional(context_element, "id")

        if id is None:
            error_repository.insert(ErrorCode.IXBRL_CONTEXT_WITHOUT_ID, context_element)
            id = str(id)

        if id in taken_ids:
            error_repository.insert(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, context_element, id=id
            )

        taken_ids.add(id)

        context = parse_context_xml(filing_context, context_element, [])
        if not context:
            continue

        successfully_added = context_repository.insert_context(context)
        if not successfully_added:
            error_repository.insert(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, context_element, id=id
            )


def parse_units(
    unit_elements: list[_Element], filing_context: FilingContext, taken_ids: Set[str]
) -> None:
    characteristic_repository = filing_context.get_characteristic_repository()
    error_repository = filing_context.get_error_repository()
    for unit_element in unit_elements:
        id = get_str_attribute_optional(unit_element, "id")

        if id is None:
            error_repository.insert(ErrorCode.IXBRL_UNIT_WITHOUT_ID, unit_element)

        if id in taken_ids:
            error_repository.insert(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, unit_element, id=id
            )

        taken_ids.add(str(id))

        unit = parse_unit_from_xml(filing_context, unit_element)
        if not unit:
            continue

        characteristic_repository.upsert(unit.get_name(), unit)


def parse_instance_elements(
    etrees: list[_Element],
) -> Tuple[List[_Element], List[_Element], List[_Element]]:
    fact_elements, footnote_elements, continuation_elements = [], [], []
    for xbrl_instance in etrees:
        facts = find_elements(xbrl_instance, ".//ix:nonNumeric | .//ix:nonFraction")
        footnotes = find_elements(xbrl_instance, ".//ix:footnote")
        continuations = find_elements(xbrl_instance, ".//ix:continuation")

        fact_elements += facts
        footnote_elements += footnotes
        continuation_elements += continuations

    return fact_elements, footnote_elements, continuation_elements


def parse_facts(
    fact_elements: list[_Element],
    continuation_chains: Dict[_Element, list[_Element]],
    filing_context: FilingContext,
    taken_ids: Set[str],
) -> None:
    context_repository = filing_context.get_context_repository()
    characteristics_repository = filing_context.get_characteristic_repository()
    report_element_repository = filing_context.get_report_element_repository()
    fact_repository = filing_context.get_fact_repository()
    error_repository = filing_context.get_error_repository()

    for fact_element in fact_elements:
        element_tag = get_prefix_localname_tag(fact_element)
        fact_id = get_str_attribute_optional(fact_element, "id")
        characteristics: List[UnitCharacteristic | ConceptCharacteristic] = []

        concept_name = get_str_attribute_optional(fact_element, "name")
        if concept_name is None:
            error_repository.insert(
                ErrorCode.IXBRL_FACT_WITHOUT_CONCEPT_NAME,
                fact_element,
                fact_id=str(fact_id),
            )
            continue

        concept_qname = qname_from_str(concept_name, fact_element)
        try:
            report_element = report_element_repository.get_typed_by_qname(
                concept_qname, Concept
            )
        except Exception:
            error_repository.insert(
                ErrorCode.IXBRL_FACT_INVALID_CONCEPT,
                fact_element,
                concept_name=concept_name,
                fact_id=str(fact_id),
            )
            continue

        else:
            concept_characteristic = ConceptCharacteristic(report_element)
            characteristics_repository.upsert(concept_name, concept_characteristic)
            characteristics.append(concept_characteristic)

        unit_id = get_str_attribute_optional(fact_element, "unitRef")

        if unit_id:
            try:
                unit_characteristic = characteristics_repository.get(
                    unit_id, UnitCharacteristic
                )
                characteristics.append(unit_characteristic)
            except ValueError:
                error_repository.insert(
                    ErrorCode.IXBRL_INVALID_FACT_UNIT_ID,
                    fact_element,
                    unit_id=unit_id,
                    fact_id=str(fact_id),
                )
        elif not unit_id and element_tag == "ix:nonFraction":
            error_repository.insert(
                ErrorCode.IXBRL_NON_FRACTION_WITHOUT_UNIT,
                fact_element,
                fact_id=str(fact_id),
            )

        context_id = get_str_attribute_optional(fact_element, "contextRef")

        if context_id is None:
            error_repository.insert(
                ErrorCode.IXBRL_FACT_WITHOUT_CONTEXT,
                fact_element,
                fact_id=str(fact_id),
            )
            continue

        context = context_repository.get_context_copy(context_id)
        if not context:
            error_repository.insert(
                ErrorCode.IXBRL_INVALID_FACT_CONTEXT_ID,
                fact_element,
                context_id=context_id,
            )
            continue

        for characteristic in characteristics:
            context._add_characteristic(characteristic)

        if element_tag == "ix:nonNumeric":
            continuation_chain = continuation_chains.get(fact_element) or []
            fact = parse_non_numeric_fact_element(
                fact_element, context, continuation_chain, filing_context, taken_ids
            )
        elif element_tag == "ix:nonFraction":
            fact = parse_non_fraction_fact_element(
                fact_element, context, filing_context, taken_ids
            )

        if fact is not None:
            fact_repository.upsert(fact)


def parse_facts_xhtml(filing_context: FilingContext) -> XHTMLFootnoteNetworkElements:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    """
    xml_service = filing_context.get_xml_service()
    error_repository = filing_context.get_error_repository()

    etrees: list[_Element] = [
        tree.getroot()
        for tree in xml_service.get_all_etrees()
        if (
            not tree.getroot().tag.endswith("schema")
            and not tree.getroot().tag.endswith("linkbase")
        )
    ]

    hidden_elements, resources_elements, references_elements = parse_headers(
        etrees, error_repository
    )

    # TODO: Move taken_ids to filing context
    taken_ids: Set[str] = set()
    parse_references_elements(references_elements, taken_ids, filing_context)

    (
        relationship_elements,
        role_ref_elements,
        arcrole_ref_elements,
        context_elements,
        unit_elements,
    ) = parse_resources_elements(resources_elements, filing_context)

    parse_contexts(context_elements, filing_context, taken_ids)
    parse_units(unit_elements, filing_context, taken_ids)
    validate_hidden_elements(hidden_elements, filing_context)

    fact_elements, footnote_elements, continuation_elements = parse_instance_elements(
        etrees
    )
    continuation_chains = create_continuation_chains(
        fact_elements,
        footnote_elements,
        continuation_elements,
        error_repository,
        taken_ids,
    )
    parse_facts(fact_elements, continuation_chains, filing_context, taken_ids)

    return XHTMLFootnoteNetworkElements(
        footnote_elements,
        continuation_chains,
        relationship_elements,
        role_ref_elements,
        arcrole_ref_elements,
        taken_ids,
    )


if __name__ == "__main__":
    data = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">1 <b> <d> b </d> </b> 2 <c> c </c> 4 </xs:schema>'
    root = etree.fromstring(data)
    root.remove(root[1])
    print(etree.tostring(root))
