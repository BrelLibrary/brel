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

from typing import Any, List, Optional, cast

from brel import Context
from brel.reportelements import Concept
from brel.characteristics import (
    Aspect,
    ICharacteristic,
    ConceptCharacteristic,
    PeriodCharacteristic,
    UnitCharacteristic,
    EntityCharacteristic,
)
from brel.services.translation.translation_service import TranslationService


class Fact:
    """
    The Fact class consists of a value, a context, id, and the precision and decimals of the fact.

    - The value is the value of the fact. It is a string.
    - The context is the context of the fact. It is a Context object.
    - The id is the id of the fact. It is a string and is optional.
    - The precision is the precision of the fact. Only used when it is a numerical fact. Only one of precision and decimals can be set.
    - The decimals is the decimals of the fact. Only used when it is a numerical fact. Only one of precision and decimals can be set.
    """

    def __init__(
        self,
        context: Context,
        value: str,
        id: str | None,
        decimals: float | None = None,
        precision: float | None = None,
    ) -> None:
        self.__precision = precision
        self.__decimals = decimals
        self.__id = id
        self.__context: Context = context
        self.__value: str = value

    def _get_id(self) -> str | None:
        """[DEPRECATED] Use get_id() instead."""
        return self.get_id()

    def get_id(self) -> str | None:
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
        """[DEPRECATED] Use str() instead."""
        return self.__value

    def get_value_as_int(self) -> int:
        """[DEPRECATED] Use int() instead."""
        return int(self)

    def __int__(self) -> int:
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
        """[DEPRECATED] Use float() instead."""
        return float(self)

    def __float__(self) -> float:
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
        """[DEPRECATED] Use bool() instead."""
        return bool(self)

    def __bool__(self) -> bool:
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
                f"Fact {self.__id} does not have a bool value. It has value {self.__value}, which does not resolve to a bool."
            )

    def get_value(self) -> Any:
        """
        :returns Any: The value of the fact. The type of the value depends on the type of the fact.
        """
        if self.get_concept().is_integer():
            return int(self)
        elif self.get_concept().is_numeric():
            return float(self)
        elif self.get_concept().is_boolean():
            return bool(self)
        else:
            return self.__value

    def get_precision(self) -> float | None:
        """
        :returns float: The precision of the fact. Only applies to numeric facts.
        """
        return self.__precision

    def get_decimals(self) -> float | None:
        """
        :returns float: The decimals property of the fact. Only applies to numeric facts.
        """
        return self.__decimals

    def __str__(self) -> str:
        """
        :returns str: The fact value as a string.
        """
        return self.__value

    # 2nd class citizens
    def get_concept(self) -> Concept:
        """
        :returns Concept: The concept of the facts context.
        Equivalent to calling `fact.get_context().get_concept().get_value()`
        """
        concept_characteristic = cast(
            ConceptCharacteristic, self.__context.get_characteristic(Aspect.CONCEPT)
        )
        concept: Concept = cast(
            Concept,
            concept_characteristic.get_value(),
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

    def get_entity(self) -> EntityCharacteristic | None:
        """
        :returns EntityCharacteristic|None: The entity characteristic of the facts context. Returns None if the fact does not have an entity.
        Equivalent to calling `fact.get_context().get_entity()`
        """
        entity: EntityCharacteristic = cast(
            EntityCharacteristic,
            self.__context.get_characteristic(Aspect.ENTITY),
        )
        return entity

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

    def __iter__(self):
        return iter(self.convert_to_dict().items())

    def convert_to_dict(
        self,
        languages: Optional[List[str]] = None,
        translation_service: Optional[TranslationService] = None,
    ) -> dict[str, Any]:
        """
        :returns dict[str, Any]: The fact represented as a dictionary. The dictionary has the following keys:
        - "id": The id of the fact. Returns None if the fact does not have an id.
        - "value": The value of the fact.
        - "context": The context of the fact represented as a dictionary.
        """
        dict_to_return = self.__context.convert_to_df_row(
            languages, translation_service
        )

        if not languages or not translation_service:
            dict_to_return["id"] = self.__id if self.__id else ""
            dict_to_return["value"] = self.__value
        else:
            id_literal = translation_service.get("literal:id", languages)
            value_literal = translation_service.get("literal:value", languages)

            if self.__id:
                dict_to_return[id_literal] = self.__id
            else:
                dict_to_return[id_literal] = translation_service.get(
                    "literal:none", languages
                )

            dict_to_return[value_literal] = self.__value

        return dict_to_return
