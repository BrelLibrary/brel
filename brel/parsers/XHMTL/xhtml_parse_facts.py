"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

from typing import cast
from lxml.etree import _Element  # type: ignore
from brel import Context, Fact
from brel.characteristics import *
from brel.contexts.filing_context import FilingContext
from brel.parsers.XML.characteristics import parse_unit_from_xml
from brel.parsers.XML.xml_context_parser import parse_context_xml
from brel.parsers.utils.error_utils import error_on_none
from brel.parsers.utils.lxml_utils import (
    find_elements,
    get_str_attribute,
    get_str_attribute_optional,
)
from brel.parsers.utils.optional_utils import get_or_raise
from brel.qnames.qname_utils import qname_from_str
from brel.reportelements import Concept


def parse_fact_from_ixbrl(
    filing_context: FilingContext,
    continuations: list[_Element],
    fact_xml_element: _Element,
    context: Context,
) -> None:
    """
    Create a single Fact from an lxml.etree._Element.
    :param continuations: The list of all the continuation facts
    :param fact_xml_element: The lxml.etree._Element to create the Fact from.
    :param context: The context of the fact. Note that new characteristics will be added to the context.
    :returns: The newly created Fact.
    """

    fact_id = get_str_attribute(fact_xml_element, "id")
    fact_concept_name = get_str_attribute(fact_xml_element, "name")
    fact_value: str = fact_xml_element.text or ""

    fact_unit_ref = get_str_attribute_optional(fact_xml_element, "unitRef")

    context_unit = get_or_raise(
        context.get_characteristic(Aspect.UNIT),
        Exception("Fact has no unit characteristic"),
    )

    if (
        context_unit
        and fact_unit_ref
        and context_unit
        and fact_unit_ref != context_unit.get_value()
    ):
        raise ValueError(
            f"Fact {fact_id} has unit {fact_unit_ref} but should have unit {context_unit.get_value()}"
        )

    # check if the fact has the correct concept
    context_concept: ConceptCharacteristic = cast(
        ConceptCharacteristic, context.get_characteristic(Aspect.CONCEPT)
    )
    if fact_concept_name != context_concept.get_value().get_name().clark_notation():
        raise ValueError(
            f"Fact {fact_id} has concept {fact_concept_name} but should have concept {context_concept.get_value().get_name().clark_notation()}"
        )

    # Check the format and apply the necessary formatting
    if (
        fact_xml_element.tag == "ix:nonFraction"
        or fact_xml_element.tag == "{http://www.xbrl.org/2013/inlineXBRL}nonFraction"
    ):
        fact_format = get_str_attribute(fact_xml_element, "format")
        fact_scale = get_str_attribute(fact_xml_element, "scale")
        if fact_format == "ixt:fixed-empty":
            fact_value = ""
        elif fact_format == "ixt:fixed-false":
            fact_value = "false"
        elif fact_format == "ixt:fixed-true":
            fact_value = "true"
        elif fact_format == "ixt:fixed-zero":
            fact_value = "0"
        elif fact_format == "ixt:num-dot-decimal":
            fact_value = fact_value.replace(",", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace(".", "").replace(" ", "").replace(",", ".")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace(",", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-dot-decimal-apos":
            fact_value = fact_value.replace("'", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace("'", "").replace(" ", "").replace(",", ".")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        elif fact_format == "ixt:num-comma-decimal":
            fact_value = fact_value.replace("'", "").replace(" ", "")
            fact_value = str(float(fact_value) * pow(10, int(fact_scale)))
        else:
            raise ValueError(f"Fact format {fact_format} not yet supported by XBRL")

    # Aggregate the continuation facts
    try:
        if fact_xml_element.get("continuedAt"):
            cont = list(
                filter(
                    lambda x: x.get("id") == fact_xml_element.get("continuedAt"),
                    continuations,
                )
            )[0]
            fact_value += cont.text  # type: ignore
    except:
        pass

    fact = Fact(context, fact_value, fact_id)  # type: ignore
    fact_repository = filing_context.get_fact_repository()
    fact_repository.upsert(fact)


def parse_facts_xhtml(filing_context: FilingContext) -> None:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    """

    report_element_repository = filing_context.get_report_element_repository()
    characteristics_repository = filing_context.get_characteristic_repository()
    xml_service = filing_context.get_xml_service()

    etrees = xml_service.get_all_etrees()

    for xbrl_instance in etrees:
        # ix_facts = xbrl_instance.findall(
        #     ".//ix:nonNumeric | .//ix:nonFraction | .//ix:fraction",  # ix:continuation - add it to something, ix:exclude - remove all things in there
        #     namespaces={"ix": "http://www.xbrl.org/2013/inlineXBRL"},
        # )
        ix_facts = find_elements(
            xbrl_instance,
            ".//ix:nonNumeric | .//ix:nonFraction | .//ix:fraction",
        )

        # continuations = xbrl_instance.findall(
        #     ".//ix:continuation",  # ix:continuation - add it to something, ix:exclude - remove all things in there
        #     namespaces={"ix": "http://www.xbrl.org/2013/inlineXBRL"},
        # )
        continuations = find_elements(
            xbrl_instance,
            ".//ix:continuation",
        )

        for ix_fact in ix_facts:
            characteristics: list[UnitCharacteristic | ConceptCharacteristic] = []

            # ======== PARSE THE CONCEPT ========
            concept_name = get_str_attribute(ix_fact, "name")

            concept_characteristic = characteristics_repository.get_or_create(
                concept_name,
                ConceptCharacteristic,
                lambda: ConceptCharacteristic(
                    report_element_repository.get_typed_by_qname(
                        qname_from_str(concept_name, ix_fact),
                        Concept,
                    )
                ),
            )
            characteristics.append(concept_characteristic)

            # ======== PARSE THE UNIT ========
            unit_id = get_str_attribute_optional(ix_fact, "unitRef")

            if unit_id:
                unit_xml = error_on_none(
                    xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']"),
                    f"Could not find unit {unit_id} in xbrl instance {xbrl_instance}",
                )

                unit_characteristic = characteristics_repository.get_or_create(
                    unit_id,
                    UnitCharacteristic,
                    lambda: parse_unit_from_xml(
                        filing_context,
                        unit_xml,
                    ),
                )
                characteristics.append(unit_characteristic)

            # ======== PARSE THE CONTEXT ========
            context_id = get_str_attribute(ix_fact, "contextRef")
            xml_context = error_on_none(
                xbrl_instance.find(f"{{*}}context[@id='{context_id}']"),
                f"Could not find context {context_id} in xbrl instance {xbrl_instance}",
            )
            fact_context = parse_context_xml(
                filing_context,
                xml_context,
                characteristics,
            )

            parse_fact_from_ixbrl(filing_context, continuations, ix_fact, fact_context)
