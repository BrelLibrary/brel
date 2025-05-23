"""
This module contains the Aspect class.
Aspects are the building blocks of the [Context](./contexts.md) of a fact.
They are split into two categories: core aspects and custom aspects.

Core aspects are the 5 base aspects: concept, period, entity and unit.

Custom aspects are all other aspects that are not core aspects.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 12 May 2025

====================
"""

from brel.resource import BrelLabel


class Aspect:
    """
    Base class for all aspects.
    An an aspect is a wrapper around a string-id.
    This string-id is called the name of the aspect.
    An aspect can also have human readable labels for its name.
    The four core aspects are instances of this class and are accessible as class attributes.

    These four core aspects are available as the following class attributes:

    - `Aspect.CONCEPT`
    - `Aspect.PERIOD`
    - `Aspect.ENTITY`
    - `Aspect.UNIT`

    A lot of reports omit the language aspect, but it can be emulated by using a custom aspect.
    All but the concept aspect are optional for a context.

    """

    CONCEPT: "Aspect"
    PERIOD: "Aspect"
    ENTITY: "Aspect"
    UNIT: "Aspect"

    def __init__(self, name: str, labels: list[BrelLabel]) -> None:
        self.__name = name
        self.__labels = labels
        self.__is_core = False

    # first class citizens
    def get_name(self) -> str:
        """
        Get the name of the aspect.
        """
        return self.__name

    def is_core(self) -> bool:
        """
        Check if the aspect is a core aspect.
        """
        return self.__is_core

    def _make_core(self) -> None:
        """
        Make the aspect a core aspect.
        """
        self.__is_core = True

    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the aspect.
        """
        return self.__labels

    def __hash__(self) -> int:
        return hash(self.__name)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Aspect):
            return self.__name == __value.get_name()
        return False

    # second class citizens
    def __str__(self) -> str:
        return self.__name


# initialize the core aspects
concept_labels = [
    BrelLabel("Concept [Axis]", "concept", "en-US"),
    BrelLabel("Konzept [Achse]", "concept", "de-DE"),
    BrelLabel("Concepto [Eje]", "concept", "es-ES"),
]

period_labels = [
    BrelLabel("Period [Axis]", "period", "en-US"),
    BrelLabel("Periode [Achse]", "period", "de-DE"),
    BrelLabel("Periodo [Eje]", "period", "es-ES"),
]

entity_labels = [
    BrelLabel("Entity [Axis]", "entity", "en-US"),
    BrelLabel("Organisation [Achse]", "entity", "de-DE"),
    BrelLabel("Entidad [Eje]", "entity", "es-ES"),
]

unit_labels = [
    BrelLabel("Unit [Axis]", "unit", "en-US"),
    BrelLabel("Einheit [Achse]", "unit", "de-DE"),
    BrelLabel("Unidad [Eje]", "unit", "es-ES"),
]

Aspect.CONCEPT = Aspect("concept", concept_labels)
Aspect.PERIOD = Aspect("period", period_labels)
Aspect.ENTITY = Aspect("entity", entity_labels)
Aspect.UNIT = Aspect("unit", unit_labels)

Aspect.CONCEPT._make_core()  # type: ignore
Aspect.PERIOD._make_core()  # type: ignore
Aspect.ENTITY._make_core()  # type: ignore
Aspect.UNIT._make_core()  # type: ignore
