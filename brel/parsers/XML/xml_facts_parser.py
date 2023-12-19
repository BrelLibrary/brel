"""
This module contains the function to parse the facts from the xbrl instance.
It parses XBRL in the XML syntax.

@author: Robin Schmidiger
@version: 0.4
@date: 19 December 2023
"""

import lxml
import lxml.etree

from brel.reportelements import IReportElement, Concept
from brel.characteristics import *
from brel import QName, QNameNSMap, Context, Fact
from typing import cast

from .xml_context_parser import parse_context_xml

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
            raise ValueError(f"Fact {fact_id} has no value but the concept {concept.get_name()} is not nillable")
        
        fact_value = ""

    fact_context_ref = fact_xml_element.get("contextRef", default=None)
    fact_unit_ref = fact_xml_element.get("unitRef", default=None)

    # check if the fact has the correct context
    if fact_context_ref != context._get_id():
        raise ValueError(f"Fact {fact_id} has context {fact_context_ref} but should have context {context._get_id()}")

    # check if the fact has the correct unit
    # Note that the unit_ref is only the local name of the unit whilst the context_unit is the full QName. 
    context_unit: UnitCharacteristic = cast(UnitCharacteristic, context.get_characteristic(BrelAspect.UNIT))
    if context_unit and fact_unit_ref and context_unit and fact_unit_ref != context_unit.get_value().get_local_name():
        raise ValueError(f"Fact {fact_id} has unit {fact_unit_ref} but should have unit {context_unit.get_value()}")
    
    # check if the fact has the correct concept
    context_concept: ConceptCharacteristic = cast(ConceptCharacteristic, context.get_characteristic(BrelAspect.CONCEPT))
    if fact_concept_name != context_concept.get_value().get_name().resolve():
        raise ValueError(f"Fact {fact_id} has concept {fact_concept_name} but should have concept {context_concept.get_value().get_name().resolve()}")

    return Fact(context, fact_value, fact_id)


def parse_facts_xml(
        etrees: list[lxml.etree._ElementTree],
        report_elements: dict[QName, IReportElement],
        qname_nsmap: QNameNSMap
        ) -> tuple[list[Fact], dict[str, Fact]]:
    """
    Parse the facts.
    :param etrees: The xbrl instance xml trees
    :param report_elements: The report elements
    :param qname_nsmap: The qname to namespace map
    :return: A list of facts and a mapping from fact ids to facts
    """
    characteristics_cache: dict[str, ICharacteristic|BrelAspect] = {}

    facts: list[Fact] = []
    id_to_fact: dict[str, Fact] = {}

    nsmap = qname_nsmap.get_nsmap()

    for xbrl_instance in etrees:

        # get all xml elements in the instance that have a contextRef attribute
        xml_facts = xbrl_instance.findall(".//*[@contextRef]", namespaces=None)

        for xml_fact in xml_facts:

            # then get the context id and search for the xbrlicontext xml element
            context_id = xml_fact.get("contextRef")
            if context_id is None:
                raise ValueError(f"Fact {xml_fact} has no contextRef attribute")
            

            # the context xml element has the tag context and the id is the context_id
            xml_context = xbrl_instance.find(f"{{*}}context[@id='{context_id}']", namespaces=nsmap)
            if xml_context is None:
                raise ValueError(f"Context {context_id} not found in xbrl instance")

            # get the unit id
            unit_id = xml_fact.get("unitRef")

            # get the unit and concept characteristics
            # Not all of the characteristics of a context are part of the "syntactic context" xml element
            # These characteristics need to be searched for in the xbrl instance, parsed separately and added to the context
            # These characteristics are the concept (mandatory) and the unit (optional)
            characteristics: list[UnitCharacteristic | ConceptCharacteristic] = []

            # if there is a unit id, then find the unit xml element, parse it and add it to the characteristics list
            if unit_id:
                # check cache
                if unit_id in characteristics_cache:
                    if not isinstance(characteristics_cache[unit_id], UnitCharacteristic):
                        raise ValueError(f"Unit {unit_id} is not a unit")

                    unit_characteristic: UnitCharacteristic = cast(UnitCharacteristic, characteristics_cache[unit_id])
                else:
                    # if not in cache, parse the unit
                    xml_unit = xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']")
                    if xml_unit is None:
                        raise ValueError(f"Unit {unit_id} not found in xbrl instance")
                    
                    unit_characteristic = UnitCharacteristic.from_xml(xml_unit, qname_nsmap)
                    characteristics_cache[unit_id] = unit_characteristic
                
                characteristics.append(unit_characteristic)

            # get the concept name              
            concept_name = xml_fact.tag                
            concept_qname = QName.from_string(concept_name, qname_nsmap)

            # check cache
            if concept_qname in characteristics_cache:
                if not isinstance(characteristics_cache[concept_qname.resolve()], ConceptCharacteristic):
                    raise ValueError(f"Concept {concept_qname} is not a concept")

                concept_characteristic = cast(ConceptCharacteristic, characteristics_cache[concept_qname.resolve()])
            else:
                # the concept has to be in the report elements cache. otherwise it does not exist
                if concept_qname not in report_elements.keys():
                    raise ValueError(f"Concept {concept_qname} not found in report elements")
                
                # wrap the concept in a characteristic
                concept = cast(Concept, report_elements[concept_qname])

                if concept is None:
                    raise ValueError(f"Concept {concept_qname} not found in report elements")
                
                if not isinstance(concept, Concept):
                    raise ValueError(f"Concept {concept_qname} is not a concept")

                concept_characteristic = ConceptCharacteristic(concept)

                # add the concept to the cache
                characteristics_cache[concept_qname.resolve()] = concept_characteristic
            # add the concept to the characteristic list
            characteristics.append(concept_characteristic)

            # then parse the context
            context = parse_context_xml(xml_context, characteristics, report_elements, qname_nsmap, characteristics_cache)

            # create the fact
            fact = parse_fact_from_xml(xml_fact, context)

            facts.append(fact)

            fact_id = xml_fact.get("id")
            if fact_id:
                id_to_fact[fact_id] = fact
    
    return facts, id_to_fact