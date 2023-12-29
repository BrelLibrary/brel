"""
Implements a Context of an XBRL instance.
A context is a collection of aspects and their associated values (characteristics).
Contexts are closely modeled after the open information model of XBRL.

@author: Robin Schmidiger
@version: 0.11
@date: 20 December 2023
"""

from brel.characteristics import BrelAspect
from brel import QName
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
    an XBRL context is a collection of aspects.
    There are 5 types of aspects: concept, period, entity, unit and additional dimensions.
    The only required aspect is the concept
    """

    def __init__(self, context_id) -> None:
        self.__id: str = context_id

        # aspects are the axis, characteristics are the values per axis
        self.__aspects: list[BrelAspect] = []
        self.__characteristics: dict[BrelAspect, ICharacteristic] = {}

        self.__aspects.sort(key=lambda aspect: aspect.get_name())

    # First class citizens
    def get_aspects(self) -> list[BrelAspect]:
        """
        Get the aspects of the context.
        :returns: A list of all the aspects of the context.
        """
        return self.__aspects

    def get_characteristic(self, aspect: BrelAspect) -> ICharacteristic | None:
        """
        Get the value of an aspect.
        """
        return next((c for a, c in self.__characteristics.items() if a == aspect), None)

    # Second class citizens
    def has_characteristic(self, aspect: BrelAspect) -> bool:
        """
        Check if the context has a certain aspect.
        :param aspect: The aspect to check for.
        :returns: True if the context has the aspect, False otherwise.
        """
        return any(aspect == context_aspect for context_aspect in self.__aspects)

    def get_characteristic_as_str(self, aspect: BrelAspect) -> str:
        """
        Get the value of an aspect as a string.
        This is a convenience function.
        The representation of aspects as strings is not standardized.
        If the aspect is not present in the context, an empty string is returned.
        :param aspect: The aspect to get the value of.
        :returns: The value of the aspect as a string.
        """
        characteristic = self.get_characteristic(aspect)
        if characteristic is None:
            return ""
        else:
            return characteristic.get_value().__str__()

    # TODO: implement
    def get_characteristic_as_qname(self, aspect: BrelAspect) -> QName:
        raise NotImplementedError()

    def get_characteristic_as_int(self, aspect: BrelAspect) -> int:
        raise NotImplementedError()

    def get_characteristic_as_float(self, aspect: BrelAspect) -> float:
        raise NotImplementedError()

    def get_characteristic_as_bool(self, aspect: BrelAspect) -> bool:
        raise NotImplementedError()

    def get_concept(self) -> ConceptCharacteristic:
        """
        Get the concept of the context.
        """
        return cast(ConceptCharacteristic, self.get_characteristic(BrelAspect.CONCEPT))

    def get_period(self) -> PeriodCharacteristic | None:
        """
        Get the period of the context.
        """
        return cast(PeriodCharacteristic, self.get_characteristic(BrelAspect.PERIOD))

    def get_entity(self) -> EntityCharacteristic | None:
        """
        Get the entity of the context.
        """
        return cast(EntityCharacteristic, self.get_characteristic(BrelAspect.ENTITY))

    def get_unit(self) -> UnitCharacteristic | None:
        """
        Get the unit of the context.
        """
        return cast(UnitCharacteristic, self.get_characteristic(BrelAspect.UNIT))

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
