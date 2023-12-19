"""
Contains the Fact class.
This class represents an XBRL fact in the Open Information Model.

@author: Robin Schmidiger
@version: 0.3
@date: 19 December 2023
"""

from typing import Any
import lxml
import lxml.etree

from brel import Context, QName
from brel.characteristics import ConceptCharacteristic, UnitCharacteristic, PeriodCharacteristic, BrelAspect
from typing import cast

class Fact:
    """
    Class for representing an XBRL fact in the Open Information Model.
    Facts consist of a value, a context and an id
    """
    
    def __init__(self, context: Context, value: str, id: str | None) -> None:
        """
        Initialize the fact.
        :param context: The context of the fact.
        :param value: The value of the fact.
        :param id: The id of the fact. The id is optional.
        """
        self.__id = id
        self.__context : Context = context
        self.__value : str = value
    
    # first class citizens
    def _get_id(self) -> str | None:
        """
        :returns: The id of the fact. Returns None if the fact does not have an id.
        """
        return self.__id
    
    def get_context(self) -> Context:
        """
        :returns: The context of the fact as a Context object.
        """
        return self.__context
    
    def get_value_as_str(self) -> str:
        """
        :returns: The value of the fact as a string.
        """
        return self.__value
    
    def get_value_as_qname(self) -> QName:
        """
        :returns: The value of the fact as a QName
        """
        # TODO: implement
        raise NotImplementedError
    
    def get_value_as_int(self) -> int:
        """
        :returns: The value of the fact as an int
        """
        try:
            return int(self.__value)
        except ValueError:
            raise ValueError(f"Fact {self.__id} does not have an int value. It has value {self.__value}, which does not resolve to an int")
    
    def get_value_as_float(self) -> float:
        """
        :returns: The value of the fact as a float
        """
        try:
            return float(self.__value)
        except ValueError:
            raise ValueError(f"Fact {self.__id} does not have a float value. It has value {self.__value}, which does not resolve to a float")
    
    def get_value_as_bool(self) -> bool:
        """
        :returns: The value of the fact as a bool
        """
        if self.__value.upper() == "TRUE":
            return True
        elif self.__value.upper() == "FALSE":
            return False
        else:
            raise ValueError(f"Fact {self.__id} does not have a bool value. It has value {self.__value}, which does not resolve to a bool")
    
    def get_value(self) -> Any:
        """
        :returns: The value of the fact. The type of the value depends on the type of the fact.
        """
        return self.__value

    
    def __str__(self) -> str:
        """
        :returns: The fact as a string.
        """
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
        :returns: The concept of the fact as a ConceptCharacteristic object. Facts always have a concept.
        """
        concept: ConceptCharacteristic = cast(ConceptCharacteristic, self.__context.get_characteristic(BrelAspect.CONCEPT))
        return concept

    def get_unit(self) -> UnitCharacteristic:
        """
        :returns: The unit of the fact as a UnitCharacteristic object. Returns None if the fact does not have a unit.
        """
        unit: UnitCharacteristic = cast(UnitCharacteristic, self.__context.get_characteristic(BrelAspect.UNIT))
        return unit

    def get_period(self) -> PeriodCharacteristic:
        """
        :returns: The period of the fact as a PeriodCharacteristic object. Returns None if the fact does not have a period.
        """
        period: PeriodCharacteristic = cast(PeriodCharacteristic, self.__context.get_characteristic(BrelAspect.PERIOD))
        return period