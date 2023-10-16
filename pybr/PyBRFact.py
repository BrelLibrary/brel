from typing import Any
import lxml
import lxml.etree
from prettytable import PrettyTable
from pybr import PyBRContext, PyBRConcept, PyBRUnit, PyBRAspect, PyBRPeriod
from typing import cast

class PyBRFact:
    """
    Class for representing an XBRL fact.
    An XBRL fact is a combination of a context and a value.
    The context contains the concept, unit, period, entity and additional dimensions.
    It also has a unique id.
    """

    __fact_cache = {}
    
    def __init__(self, id, context : PyBRContext, value) -> None:
        self.__id = id
        self.__context : PyBRContext = context
        self.__value = value

        self.__fact_cache[id] = self
    
    def get_id(self) -> str:
        return self.__id
    
    def get_context(self) -> PyBRContext:
        return self.__context
    
    def get_value(self) -> str:
        return self.__value
    
    def __str__(self) -> str:
        output = ""
        for aspect in self.__context.get_aspects():
            aspect_name = aspect.get_name()
            aspect_value = self.__context.get_value_as_object(aspect)
            output += f"{aspect_name}: {aspect_value}, "
        output += f"value: {self.__value}"
        return output

    @classmethod
    def from_xml(cls, 
            fact_xml_element: lxml.etree._Element,
            context: PyBRContext,
            ) -> "PyBRFact":
        """
        Create a PyBRFact from an lxml.etree._Element.
        """
        fact_id = fact_xml_element.attrib["id"]

        if fact_id in cls.__fact_cache:
            return cls.__fact_cache[fact_id]

        fact_concept_name = fact_xml_element.tag
        fact_value = fact_xml_element.text
        # fact_context_ref = xml_element.attrib["contextRef"]
        # fact_unit_ref = xml_element.attrib["unitRef"]
        fact_context_ref = fact_xml_element.get("contextRef", default=None)
        fact_unit_ref = fact_xml_element.get("unitRef", default=None)

        # check if the fact has the correct context
        if fact_context_ref != context.get_id():
            raise ValueError(f"Fact {fact_id} has context {fact_context_ref} but should have context {context.get_id()}")
    
        # check if the fact has the correct unit
        context_unit:PyBRUnit = cast(PyBRUnit, context.get_value_as_object(PyBRAspect.UNIT))
        if context_unit and fact_unit_ref and context_unit and fact_unit_ref != context_unit.get_name():
            raise ValueError(f"Fact {fact_id} has unit {fact_unit_ref} but should have unit {context_unit.get_name()}")
        
        # check if the fact has the correct concept
        context_concept:PyBRConcept = cast(PyBRConcept, context.get_value_as_object(PyBRAspect.CONCEPT))
        if fact_concept_name != context_concept.get_name().resolve():
            raise ValueError(f"Fact {fact_id} has concept {fact_concept_name} but should have concept {context_concept.get_name().resolve()}")

        return cls(fact_id, context, fact_value)
    
    # TODO: the concept has a periodType and a type. The fact should be validated against those.
    # In general, improve the tie in with PyBRConcept

    # 2nd class citizens
    def get_concept(self) -> PyBRConcept:
        concept: PyBRConcept = cast(PyBRConcept, self.__context.get_value_as_object(PyBRAspect.CONCEPT))
        if not concept:
            raise ValueError(f"Fact {self.__id} does not have a concept")

        return concept

    def get_unit(self) -> PyBRUnit:
        unit: PyBRUnit = cast(PyBRUnit, self.__context.get_value_as_object(PyBRAspect.UNIT))
        if not unit:
            raise ValueError(f"Fact {self.__id} does not have a unit")

        return unit

    def get_period(self) -> PyBRPeriod:
        period: PyBRPeriod = cast(PyBRPeriod, self.__context.get_value_as_object(PyBRAspect.PERIOD))
        if not period:
            raise ValueError(f"Fact {self.__id} does not have a period")

        return period        
    