"""
This module contains the function to parse the facts from the xbrl instance.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.9
- date: 15 April 2025

====================
"""


import lxml
import lxml.etree

from brel import Context, Fact
from brel.characteristics import *
from brel.parsers.XML.characteristics import parse_unit_from_xml
from brel.parsers.XML.xml_context_parser import parse_context_xml
from brel.parsers.utils.error_utils import error_on_none
from brel.qnames.qname_utils import qname_from_str
from brel.reportelements import Concept
from brel.contexts.filing_context import FilingContext
from brel.parsers.utils.lxml_utils import find_elements, get_str_attribute, get_str_tag


def parse_fact_from_xml(
    filingContext: FilingContext,
    fact_xml_element: lxml.etree._Element,  # type: ignore
    context: Context,
) -> None:
    """
    Create a single Fact from an lxml.etree._Element.
    :param fact_xml_element: The lxml.etree._Element to create the Fact from.
    :param context: The context of the fact. Note that new characteristics will be added to the context.
    :returns: The newly Fact.
    """
    error_repository = filingContext.get_error_repository()
    fact_repository = filingContext.get_fact_repository()

    fact_id = fact_xml_element.get("id")

    fact_concept_name = fact_xml_element.tag
    fact_value = fact_xml_element.text

    if fact_value is None:
        error_repository.upsert_if(
            context.get_concept().get_value().is_nillable(),
            ValueError(
                f"Fact {fact_id} has no value but the concept {fact_concept_name} is not nillable"
            ),
        )
        fact_value = ""

    fact_unit_ref = fact_xml_element.get("unitRef")
    context_unit = context.get_unit()
    if context_unit and fact_unit_ref and fact_unit_ref != context_unit.get_value():
        error_repository.upsert(
            ValueError(
                f"Fact {fact_id} has unit {fact_unit_ref} but should have unit {context_unit.get_value()}"
            )
        )

    context_concept = context.get_concept()
    if fact_concept_name != context_concept.get_value().get_name().clark_notation():
        error_repository.upsert(
            ValueError(
                f"Fact {fact_id} has concept {fact_concept_name} but should have concept {context_concept.get_value().get_name().clark_notation()}"
            )
        )

    fact_repository.upsert(Fact(context, fact_value, fact_id))


def parse_facts_xml(
    context: FilingContext,
) -> None:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    """

    report_element_repository = context.get_report_element_repository()
    characteristics_repository = context.get_characteristic_repository()
    xml_service = context.get_xml_service()

    for xbrl_instance in xml_service.get_all_etrees():
        for xml_fact in find_elements(xbrl_instance, ".//*[@contextRef]"):
            fact_characteristics: list[UnitCharacteristic | ConceptCharacteristic] = []

            # ======== PARSE THE CONCEPT ========
            concept_name = get_str_tag(xml_fact)

            concept_characteristic = characteristics_repository.get_or_create(
                concept_name,
                ConceptCharacteristic,
                lambda: ConceptCharacteristic(
                    report_element_repository.get_typed_by_qname(
                        qname_from_str(concept_name, xml_fact),
                        Concept,
                    )
                ),
            )
            fact_characteristics.append(concept_characteristic)

            # ======== PARSE THE UNIT ========
            unit_id = xml_fact.get("unitRef")

            if unit_id:
                unit_xml = error_on_none(
                    xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']"),
                    f"Could not find unit {unit_id} in xbrl instance {xbrl_instance}",
                )

                unit_characteristic = characteristics_repository.get_or_create(
                    unit_id,
                    UnitCharacteristic,
                    lambda: parse_unit_from_xml(
                        context,
                        unit_xml,
                    ),
                )
                fact_characteristics.append(unit_characteristic)

            # ======== PARSE THE CONTEXT ========
            context_id = get_str_attribute(xml_fact, "contextRef")

            xml_context = error_on_none(
                xbrl_instance.find(
                    f"{{*}}context[@id='{context_id}']", namespaces=None
                ),
                f"Could not find context {context_id} in xbrl instance {xbrl_instance}",
            )

            fact_context = parse_context_xml(context, xml_context, fact_characteristics)
            parse_fact_from_xml(context, xml_fact, fact_context)
