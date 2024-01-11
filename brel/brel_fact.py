"""
This module contains the Fact class.

Facts in Brel are the atomic pieces of information. They consist of a value, a context and an id.
They closely resemble the facts in XBRL in the Open Information Model.

To print a fact to the console, use the `pprint` function in the `brel` module.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 06 January 2024

====================
"""

from typing import Any

from brel import Context, QName
from brel.characteristics import (
    ConceptCharacteristic,
    UnitCharacteristic,
    PeriodCharacteristic,
    Aspect,
    ICharacteristic,
)
from typing import cast


class Fact:
    """
    The Fact class consists of a value, a context and an id.

    - The value is the value of the fact. It is a string.
    - The context is the context of the fact. It is a Context object.
    - The id is the id of the fact. It is a string and is optional.

    """

    def __init__(self, context: Context, value: str, id: str | None) -> None:
        self.__id = id
        self.__context: Context = context
        self.__value: str = value

    # first class citizens
    def _get_id(self) -> str | None:
        """
        :returns str|None: The id of the fact. Returns None if the fact does not have an id.
        """
        return self.__id

    def get_context(self) -> Context:
        """
        :returns Context: The context of the fact as a Context object.
        """
        return self.__context

    def get_value_as_str(self) -> str:
        """
        :returns str: The value of the fact as a string.
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
        :returns int: The value of the fact as an int
        :raises ValueError: If the value of the fact does not resolve to an int
        """
        try:
            return int(self.__value)
        except ValueError:
            raise ValueError(
                f"Fact {self.__id} does not have an int value. It has value {self.__value}, which does not resolve to an int"
            )

    def get_value_as_float(self) -> float:
        """
        :returns float: The value of the fact as a float
        :raises ValueError: If the value of the fact does not resolve to a float
        """
        try:
            return float(self.__value)
        except ValueError:
            raise ValueError(
                f"Fact {self.__id} does not have a float value. It has value {self.__value}, which does not resolve to a float"
            )

    def get_value_as_bool(self) -> bool:
        """
        :returns bool: The value of the fact as a bool
        :raises ValueError: If the value of the fact does not resolve to a bool
        """
        if self.__value.upper() == "TRUE":
            return True
        elif self.__value.upper() == "FALSE":
            return False
        else:
            raise ValueError(
                f"Fact {self.__id} does not have a bool value. It has value {self.__value}, which does not resolve to a bool"
            )

    def get_value(self) -> Any:
        """
        :returns Any: The value of the fact. The type of the value depends on the type of the fact.
        """
        return self.__value

    def __str__(self) -> str:
        """
        :returns str: The fact represented as a string.
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
        :returns ConceptCharacteristic: The concept characteristic of the facts context.
        Equivalent to calling `fact.get_context().get_concept()`
        """
        concept: ConceptCharacteristic = cast(
            ConceptCharacteristic,
            self.__context.get_characteristic(Aspect.CONCEPT),
        )
        return concept

    def get_unit(self) -> UnitCharacteristic | None:
        """
        :returns UnitCharacteristic|None: The unit characteristic of the facts context. Returns None if the fact does not have a unit.
        Equivalent to calling `fact.get_context().get_unit()`
        """
        unit: UnitCharacteristic = cast(
            UnitCharacteristic, self.__context.get_characteristic(Aspect.UNIT)
        )
        return unit

    def get_period(self) -> PeriodCharacteristic | None:
        """
        :returns PeriodCharacteristic|None: The period characteristic of the facts context. Returns None if the fact does not have a period.
        Equivalent to calling `fact.get_context().get_period()`
        """
        period: PeriodCharacteristic = cast(
            PeriodCharacteristic,
            self.__context.get_characteristic(Aspect.PERIOD),
        )
        return period

    def get_aspects(self) -> list[Aspect]:
        """
        :returns list[BrelAspect]: The aspects of the facts context.
        Equivalent to calling `fact.get_context().get_aspects()`
        """
        return self.__context.get_aspects()

    def get_characteristic(self, aspect: Aspect) -> ICharacteristic | None:
        """
        Given an aspect, get the associated characteristic of the fact.
        :param aspect: The aspect for which the characteristic should be returned.
        :returns ICharacteristic|None: The characteristic associated with the given aspect. Returns None if the fact does not have the given aspect.
        Equivalent to calling `fact.get_context().get_characteristic(aspect)`
        """
        return self.__context.get_characteristic(aspect)
