"""
This module contains the Context class.

Contexts are what puts facts into context.
For example, take the following fact:

- The Foo Corporation had a Total Revenue of 1'000'000 USD in 2020.

The context of this fact would be:

- Entity: Foo Corporation
- Period: 2020
- Concept: Total Revenue
- Unit: USD

Note that the value 1000000 is not part of the context. It is the value of the fact.

Contexts consist of aspects and their associated characteristics.
In the example above, the aspects are Entity, Period, Concept and Unit.
Characteristics are aspect-value pairs.
So for example, the characteristic of the Entity aspect would be "Foo Corporation".

Read more about Aspects and Characteristics in 

====================

- author: Robin Schmidiger
- version: 0.12
- date: 07 January 2024

====================
"""

from brel.characteristics import Aspect
from brel.characteristics import (
    ICharacteristic,
    ConceptCharacteristic,
    PeriodCharacteristic,
    EntityCharacteristic,
    UnitCharacteristic,
)
from typing import cast


class Context:
    """
    Class for representing an XBRL context.
    an XBRL context is a collection of aspects and characteristics.
    There are different types of aspects: concept, period, entity, unit and dimensions
    The only required aspect is the concept.
    All aspects can only be present once.
    Dimensions are custom aspects, so they can be present multiple times as long as they represent different dimensions.
    """

    def __init__(self, context_id) -> None:
        self.__id: str = context_id

        # aspects are the axis, characteristics are the values per axis
        self.__aspects: list[Aspect] = []
        self.__characteristics: dict[Aspect, ICharacteristic] = {}

        self.__aspects.sort(key=lambda aspect: aspect.get_name())

    # First class citizens
    def get_aspects(self) -> list[Aspect]:
        """
        Get all aspects of the context.
        :returns list[Aspect]: The aspects of the context.
        """
        return self.__aspects

    def get_characteristic(self, aspect: Aspect) -> ICharacteristic | None:
        """
        Get the value of an aspect.
        :param aspect: The aspect to get the value of.
        :returns Aspect|None: The value of the aspect. None if the aspect is not present in the context.
        """
        return next(
            (c for a, c in self.__characteristics.items() if a == aspect), None
        )

    # Second class citizens
    def has_characteristic(self, aspect: Aspect) -> bool:
        """
        Check if the context has a certain aspect.
        :param aspect: The aspect to check for.
        :returns bool: True if the context has the aspect, False otherwise.
        """
        return any(
            aspect == context_aspect for context_aspect in self.__aspects
        )

    def get_characteristic_as_str(self, aspect: Aspect) -> str:
        """
        Get the value of an aspect as a string.
        This is a convenience function.
        The representation of aspects as strings is not standardized.
        If the aspect is not present in the context, an empty string is returned.
        :param aspect: The aspect to get the value of.
        :returns str: The value of the aspect as a string.
        """
        characteristic = self.get_characteristic(aspect)
        if characteristic is None:
            return ""
        else:
            return characteristic.get_value().__str__()

    def get_characteristic_as_int(self, aspect: Aspect) -> int:
        """
        Get the value of an aspect as an int.
        This is a convenience function.
        If the aspect is not present in the context, 0 is returned.
        :param aspect: The aspect to get the value of.
        :returns int: The value of the aspect as an int.
        :raises ValueError: If the aspect is present, but the value cannot be converted to an int.
        """
        if not self.has_characteristic(aspect):
            return 0
        try:
            return int(self.get_characteristic_as_str(aspect))
        except ValueError:
            raise ValueError(
                f"Aspect {aspect} is present, but the value {self.get_characteristic_as_str(aspect)} cannot be converted to an int"
            )

    def get_characteristic_as_float(self, aspect: Aspect) -> float:
        """
        Get the value of an aspect as a float.
        This is a convenience function.
        If the aspect is not present in the context, 0.0 is returned.
        :param aspect: The aspect to get the value of.
        :returns float: The value of the aspect as a float.
        :raises ValueError: If the aspect is present, but the value cannot be converted to a float.
        """
        if not self.has_characteristic(aspect):
            return 0.0
        try:
            return float(self.get_characteristic_as_str(aspect))
        except ValueError:
            raise ValueError(
                f"Aspect {aspect} is present, but the value {self.get_characteristic_as_str(aspect)} cannot be converted to a float"
            )

    def get_characteristic_as_bool(self, aspect: Aspect) -> bool:
        """
        Get the value of an aspect as a bool.
        This is a convenience function.
        If the aspect is not present in the context, False is returned.
        :param aspect: The aspect to get the value of.
        :returns bool: The value of the aspect as a bool.
        :raises ValueError: If the aspect is present, but the value cannot be converted to a bool.
        """
        if not self.has_characteristic(aspect):
            return False
        try:
            return bool(self.get_characteristic_as_str(aspect))
        except ValueError:
            raise ValueError(
                f"Aspect {aspect} is present, but the value {self.get_characteristic_as_str(aspect)} cannot be converted to a bool"
            )

    def get_concept(self) -> ConceptCharacteristic:
        """
        Get the concept of the context.
        This function is equivalent to `get_characteristic(Aspect.CONCEPT)`.
        It cannot return None, because the concept is a required aspect.
        :returns ConceptCharacteristic: The concept of the context.
        """
        return cast(
            ConceptCharacteristic, self.get_characteristic(Aspect.CONCEPT)
        )

    def get_period(self) -> PeriodCharacteristic | None:
        """
        Get the period of the context.
        This function is equivalent to `get_characteristic(Aspect.PERIOD)`.
        :returns PeriodCharacteristic|None: The period of the context. None if the context does not have a period.
        """
        return cast(
            PeriodCharacteristic, self.get_characteristic(Aspect.PERIOD)
        )

    def get_entity(self) -> EntityCharacteristic | None:
        """
        Get the entity of the context.
        This function is equivalent to `get_characteristic(Aspect.ENTITY)`.
        :returns EntityCharacteristic|None: The entity of the context. None if the context does not have an entity.
        """
        return cast(
            EntityCharacteristic, self.get_characteristic(Aspect.ENTITY)
        )

    def get_unit(self) -> UnitCharacteristic | None:
        """
        Get the unit of the context.
        This function is equivalent to `get_characteristic(Aspect.UNIT)`.
        :returns UnitCharacteristic|None: The unit of the context. None if the context does not have a unit.
        """
        return cast(UnitCharacteristic, self.get_characteristic(Aspect.UNIT))

    # Internal methods
    def _add_characteristic(self, characteristic: ICharacteristic) -> None:
        """
        Add an aspect to the context.
        This method is for advanced users only.
        :param characteristic: The characteristic to add.
        """
        aspect = characteristic.get_aspect()

        if aspect not in self.__aspects:
            self.__aspects.append(aspect)

            self.__characteristics[aspect] = characteristic

            self.__aspects.sort(key=lambda aspect: aspect.get_name())
        else:
            pass

    def _get_id(self) -> str:
        """
        Get the id of the context.
        This is an implementation detail of the underlying XBRL library.
        It serves as a sanity check and is intended for advanced users only.
        :returns: The id of the context as a string.
        """
        return self.__id

    def __str__(self) -> str:
        output = ""
        for aspect in self.__aspects:
            output += f"{aspect} "
        return output

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Context):
            return False

        # TODO: dont use the _id, compare the aspects instead
        return self._get_id() == __value._get_id()
