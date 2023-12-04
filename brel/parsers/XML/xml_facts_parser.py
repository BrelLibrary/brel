import os
import lxml
import lxml.etree

from brel.reportelements import IReportElement, Concept
from brel.characteristics import ConceptCharacteristic, UnitCharacteristic
from brel import QName, Context, Fact
from typing import cast


def parse_facts_xml(
        xbrl_instance: lxml.etree._ElementTree,
        report_elements: dict[QName, IReportElement]
        ) -> list[Fact]:
    """
    Parse the facts.
    """
    # get all xml elements in the instance that have a contextRef attribute
    xml_facts = xbrl_instance.findall(".//*[@contextRef]", namespaces=None)

    unit_cache: dict[str, UnitCharacteristic] = {}
    concept_cache: dict[QName, ConceptCharacteristic] = {}


    facts = []
    for xml_fact in xml_facts:

        # then get the context id and search for the context xml element
        context_id = xml_fact.attrib["contextRef"]
        
        # the context xml element has the tag {{*}}context and the id is the context_id
        xml_context = xbrl_instance.find(f"{{*}}context[@id='{context_id}']")


        # get the unit id
        unit_id = xml_fact.get("unitRef")

        # get the unit and concept characteristics
        # Not all of the characteristics of a context are part of the "syntactic context" xml element
        # These characteristics need to be searched for in the xbrl instance, parsed separately and added to the context
        # These characteristics are the concept (mandatory) and the unit (optional)
        characteristics = []

        # if there is a unit id, then find the unit xml element, parse it and add it to the characteristics list
        if unit_id:
            # check cache
            if unit_id in unit_cache:
                unit_characteristic = unit_cache[unit_id]
            else:
                xml_unit = xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']")
                unit_characteristic = UnitCharacteristic.from_xml(xml_unit)
                unit_cache[unit_id] = unit_characteristic
            
            characteristics.append(unit_characteristic)

        # get the concept name              
        concept_name = xml_fact.tag                
        concept_qname = QName.from_string(concept_name)

        if concept_qname in concept_cache:
            concept_characteristic = concept_cache[concept_qname]
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
            concept_cache[concept_qname] = concept_characteristic

        # add the concept to the characteristic list
        characteristics.append(concept_characteristic)

        # then parse the context
        context = Context.from_xml(xml_context, characteristics, report_elements)

        # create the fact
        fact = Fact.from_xml(xml_fact, context)

        facts.append(fact)
    
    return facts