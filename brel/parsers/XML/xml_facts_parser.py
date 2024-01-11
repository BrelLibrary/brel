"""
This module contains the function to parse the facts from the xbrl instance.
It parses XBRL in the XML syntax.

@author: Robin Schmidiger
@version: 0.5
@date: 20 December 2023
"""

import lxml
import lxml.etree

from brel.reportelements import IReportElement, Concept
from brel.characteristics import *
from brel import QName, QNameNSMap, Context, Fact
from typing import cast

from brel.parsers.XML import parse_context_xml
from brel.parsers.XML.characteristics import parse_unit_from_xml


def parse_fact_from_xml(
    fact_xml_element: lxml.etree._Element,
    context: Context,
) -> Fact:
    """
    Create a single Fact from an lxml.etree._Element.
    :param fact_xml_element: The lxml.etree._Element to create the Fact from.
    :param context: The context of the fact. Note that new characteristics will be added to the context.
    :returns: The newly Fact.
    """
    fact_id = fact_xml_element.get("id")

    fact_concept_name = fact_xml_element.tag
    fact_value = fact_xml_element.text

    if fact_value is None:
        concept = context.get_concept().get_value()
        if not concept.is_nillable():
            raise ValueError(
                f"Fact {fact_id} has no value but the concept {concept.get_name()} is not nillable"
            )

        fact_value = ""

    fact_context_ref = fact_xml_element.get("contextRef", default=None)
    fact_unit_ref = fact_xml_element.get("unitRef", default=None)

    # check if the fact has the correct context
    if fact_context_ref != context._get_id():
        raise ValueError(
            f"Fact {fact_id} has context {fact_context_ref} but should have context {context._get_id()}"
        )

    # check if the fact has the correct unit
    # Note that the unit_ref is only the local name of the unit whilst the context_unit is the full QName.
    context_unit: UnitCharacteristic = cast(
        UnitCharacteristic, context.get_characteristic(Aspect.UNIT)
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
    if fact_concept_name != context_concept.get_value().get_name().resolve():
        raise ValueError(
            f"Fact {fact_id} has concept {fact_concept_name} but should have concept {context_concept.get_value().get_name().resolve()}"
        )

    return Fact(context, fact_value, fact_id)


def parse_facts_xml(
    etrees: list[lxml.etree._ElementTree],
    report_elements: dict[QName, IReportElement],
    qname_nsmap: QNameNSMap,
) -> tuple[list[Fact], dict[str, Fact]]:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    :param report_elements: The report elements
    :param qname_nsmap: The qname to namespace map
    :return: A list of facts and a mapping from fact ids to facts
    """

    # Since many facts share the same characteristics, we cache the characteristics and reuse them.
    # instead of passing the cache around, we use these functions to get and add characteristics to the cache
    characteristics_cache: dict[str, ICharacteristic | Aspect] = {}

    def get_from_cache(key: str) -> ICharacteristic | Aspect | None:
        if key in characteristics_cache:
            return characteristics_cache[key]
        else:
            return None

    def add_to_cache(
        key: str, characteristic: ICharacteristic | Aspect
    ) -> None:
        characteristics_cache[key] = characteristic

    # the same is true for report elements and qnames. Instead of passing dicts and nsmaps around, we use these functions
    def make_qname(qname_str: str) -> QName:
        return QName.from_string(qname_str, qname_nsmap)

    def get_report_element(qname: QName) -> IReportElement | None:
        if qname in report_elements:
            return report_elements[qname]
        else:
            return None

    # Next, we parse the facts
    facts: list[Fact] = []
    # in XBRL, some locators in networks can point to facts
    # Example: <locators href="http://www.example.com/my_schema.xsd#1234" label="some_label"/>
    # In this case, the locator points to an xml element in file my_schema.xsd with the attribute id="1234"
    # This xml element can be many things. A fact, a report element, ...
    # So we need to have a mapping from id -> fact to be able to resolve these locators
    id_to_fact: dict[str, Fact] = {}

    for xbrl_instance in etrees:
        # get all xml elements in the instance that have a contextRef attribute
        xml_facts = xbrl_instance.findall(".//*[@contextRef]", namespaces=None)

        for xml_fact in xml_facts:
            # get the unit and concept characteristics
            # Not all of the characteristics of a context are part of the "syntactic context" xml element
            # These characteristics need to be searched for in the xbrl instance, parsed separately and added to the context
            # These characteristics are the concept (mandatory) and the unit (optional)
            characteristics: list[
                UnitCharacteristic | ConceptCharacteristic
            ] = []

            # ======== PARSE THE CONCEPT ========
            # get the concept name
            concept_name = xml_fact.tag
            if concept_name is None:
                raise ValueError(f"Fact {xml_fact} has no tag")

            # check cache for concept
            concept_characteristic = get_from_cache(f"concept {concept_name}")
            if concept_characteristic is None:
                # if the concept is not in the cache, create it
                concept_qname = make_qname(concept_name)
                concept = get_report_element(concept_qname)
                if concept is None:
                    raise ValueError(
                        f"Concept {concept_qname} not found in report elements"
                    )

                if not isinstance(concept, Concept):
                    raise ValueError(
                        f"Concept {concept_qname} is not a concept. It is a {type(concept)}"
                    )

                concept_characteristic = ConceptCharacteristic(concept)
                add_to_cache(f"concept {concept_name}", concept_characteristic)
            else:
                # if the concept is in the cache, type check it
                if not isinstance(
                    concept_characteristic, ConceptCharacteristic
                ):
                    raise ValueError(
                        f"Concept {concept_name} is not a concept"
                    )

                concept_characteristic = cast(
                    ConceptCharacteristic, concept_characteristic
                )
                concept = concept_characteristic.get_value()

            # add the concept to the characteristic list
            characteristics.append(concept_characteristic)

            # ======== PARSE THE UNIT ========
            # if there is a unit id, then find the unit xml element, parse it and add it to the characteristics list
            # get the unit id
            unit_id = xml_fact.get("unitRef")

            if unit_id:
                # check cache for unit
                unit_characteristic = get_from_cache(unit_id)
                if unit_characteristic is None:
                    # create the unit if it is not in the cache
                    unit_xml = xbrl_instance.find(
                        f"{{*}}unit[@id='{unit_id}']"
                    )
                    if unit_xml is None:
                        raise ValueError(
                            f"Unit {unit_id} not found in xbrl instance"
                        )

                    unit_characteristic = parse_unit_from_xml(
                        unit_xml,
                        concept,
                        make_qname,
                        get_from_cache,
                        add_to_cache,
                    )
                    add_to_cache(unit_id, unit_characteristic)
                else:
                    # if the unit is in the cache, type check it
                    if not isinstance(unit_characteristic, UnitCharacteristic):
                        raise ValueError(f"Unit {unit_id} is not a unit")

                characteristics.append(unit_characteristic)

            # ======== PARSE THE CONTEXT ========
            # Note that there is a 1:1 mapping between facts and contexts. Therefore, if we cache facts, the contexts are cached as well.
            # First get the context id
            # This attribute is mandatory according to the XBRL specification
            context_id = xml_fact.get("contextRef")
            if context_id is None:
                raise ValueError(
                    f"Fact {xml_fact} has no contextRef attribute"
                )

            # the context xml element has the tag context and the id is the context_id
            xml_context = xbrl_instance.find(
                f"{{*}}context[@id='{context_id}']", namespaces=None
            )
            if xml_context is None:
                raise ValueError(
                    f"Context {context_id} not found in xbrl instance"
                )

            # then parse the context
            context = parse_context_xml(
                xml_context,
                characteristics,
                make_qname,
                get_report_element,
                get_from_cache,
                add_to_cache,
            )

            # create the fact
            fact = parse_fact_from_xml(xml_fact, context)

            facts.append(fact)

            # add the fact to the id_to_fact mapping if it has an id
            fact_id = xml_fact.get("id")
            if fact_id:
                id_to_fact[fact_id] = fact

    return facts, id_to_fact
