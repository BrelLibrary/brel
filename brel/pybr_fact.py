from typing import Any
import lxml
import lxml.etree

from brel import Context, QName
from brel.characteristics import ConceptCharacteristic, UnitCharacteristic, PeriodCharacteristic, BrelAspect
from typing import cast

class Fact:
    """
    Class for representing an XBRL fact.
    An XBRL fact is a combination of a context and a value.
    The context contains the concept, unit, period, entity and additional dimensions.
    It also has a unique id.
    """

    __fact_cache: dict[str, 'Fact'] = {}
    
    def __init__(self, id: str, context: Context, value: str) -> None:
        self.__id = id
        self.__context : Context = context
        self.__value : str = value

        self.__fact_cache[id] = self
    
    # first class citizens
    def _get_id(self) -> str:
        """
        @returns: The ID of the fact as a string.
        """
        return self.__id
    
    def get_context(self) -> Context:
        """
        @returns: The context of the fact as a Context object.
        """
        return self.__context
    
    def get_value_as_str(self) -> str:
        """
        @returns: The value of the fact as a string.
        """
        return self.__value
    
    def get_value_as_qname(self) -> QName:
        """
        @returns: The value of the fact as a QName
        """
        if not QName.is_str_qname(self.__value):
            raise ValueError(f"Fact {self.__id} does not have a QName value. It has value {self.__value}, which does not resolve to a QName")
        
        return QName.from_string(self.__value)
    
    def get_value_as_int(self) -> int:
        """
        @returns: The value of the fact as an int
        """
        try:
            return int(self.__value)
        except ValueError:
            raise ValueError(f"Fact {self.__id} does not have an int value. It has value {self.__value}, which does not resolve to an int")
    
    def get_value_as_float(self) -> float:
        """
        @returns: The value of the fact as a float
        """
        try:
            return float(self.__value)
        except ValueError:
            raise ValueError(f"Fact {self.__id} does not have a float value. It has value {self.__value}, which does not resolve to a float")
    
    def get_value_as_bool(self) -> bool:
        """
        @returns: The value of the fact as a bool
        """
        if self.__value.upper() == "TRUE":
            return True
        elif self.__value.upper() == "FALSE":
            return False
        else:
            raise ValueError(f"Fact {self.__id} does not have a bool value. It has value {self.__value}, which does not resolve to a bool")
    
    def get_value(self) -> Any:
        """
        @returns: The value of the fact. The type of the value depends on the type of the fact.
        """
        return self.__value

    
    def __str__(self) -> str:
        output = ""
        for aspect in self.__context.get_aspects():
            aspect_name = aspect.get_name()
            aspect_value = self.__context.get_characteristic(aspect)
            output += f"{aspect_name}: {aspect_value}, "
        output += f"value: {self.__value}"
        return output

    # 2nd class citizens
    def get_concept(self) -> ConceptCharacteristic:
        """
        @returns: The concept of the fact as a ConceptCharacteristic object.
        @raises: ValueError if the fact does not have a concept.
        """
        concept: ConceptCharacteristic = cast(ConceptCharacteristic, self.__context.get_characteristic(BrelAspect.CONCEPT))
        if not concept:
            raise ValueError(f"Fact {self.__id} does not have a concept")

        return concept

    def get_unit(self) -> UnitCharacteristic:
        """
        @returns: The unit of the fact as a UnitCharacteristic object.
        @raises: ValueError if the fact does not have a unit.
        """
        unit: UnitCharacteristic = cast(UnitCharacteristic, self.__context.get_characteristic(BrelAspect.UNIT))
        if not unit:
            raise ValueError(f"Fact {self.__id} does not have a unit")

        return unit

    def get_period(self) -> PeriodCharacteristic:
        """
        @returns: The period of the fact as a PeriodCharacteristic object.
        @raises: ValueError if the fact does not have a period.
        """
        period: PeriodCharacteristic = cast(PeriodCharacteristic, self.__context.get_characteristic(BrelAspect.PERIOD))
        if not period:
            raise ValueError(f"Fact {self.__id} does not have a period")

        return period        
    
    # internal use methods
    @classmethod
    def from_xml(cls, 
            fact_xml_element: lxml.etree._Element,
            context: Context,
            ) -> "Fact":
        """
        Create a Fact from an lxml.etree._Element.
        @param fact_xml_element: The lxml.etree._Element to create the Fact from.
        @param context: The context of the fact. Note that new characteristics will be added to the context.
        @returns: The Fact.
        """
        fact_id = fact_xml_element.attrib["id"]

        if fact_id in cls.__fact_cache:
            return cls.__fact_cache[fact_id]

        fact_concept_name = fact_xml_element.tag
        fact_value = fact_xml_element.text

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

        return cls(fact_id, context, fact_value)
    