"""
This module contains the interface for a characteristic.
Characteristics are what makes up the context of a fact.
They are a binding between an aspect and a value.

There are characteristics for the 5 core aspects.

- [`ConceptCharacteristic`](./concept-characteristic.md) for `Aspect.CONCEPT`
- [`PeriodCharacteristic`](./period-characteristic.md) for `Aspect.PERIOD`
- [`EntityCharacteristic`](./entity-characteristic.md) for `Aspect.ENTITY`
- [`UnitCharacteristic`](./unit-characteristic.md) for `Aspect.UNIT`
- [`LanguageCharacteristic`](./language-characteristic.md) for `Aspect.LANGUAGE`

There are also characteristics for custom aspects. Custom aspects can either be typed or explicit.
A explicit aspect is an aspect where the characteristic value is one option from a list of options.

For example, consider the following facts:

- The Foo Company has a revenue of 1000 USD in 2020 in the region North America.
- The Foo Company has a revenue of 2000 USD in 2020 in the region Europe.

The region aspect is an explicit aspect since the options that the region aspect can take are limited to North America and Europe.

A typed aspect is an aspect where the characteristic value is a value of a certain type.
Brel simplifies this by making the value a string and the type a QName.

For example, consider the following facts:

- The Bar Company has 8 employees that earn 1000 USD per month in 2020.
- The Bar Company has 2 employees that earn 2000 USD per month in 2020.

In this case value of the fact is the number of employees.
The type aspect is the 'salary per month' aspect, is an integer.

- [`ExplicitDimensionCharacteristic`](./explicit_dimension_characteristic.md) for explicit dimensions.
- [`TypedDimensionCharacteristic`](./typed_dimension_characteristic.md) for typed dimensions.

=================

- author: Robin Schmidiger
- version: 0.1
- date: 2023-12-06

=================
"""

from abc import ABC, abstractmethod
from brel.characteristics import Aspect
from typing import Any


class ICharacteristic(ABC):
    """
    The Interface for a characteristic.
    A characteristic is a binding between an aspect and a value.
    """

    @abstractmethod
    def get_value(self) -> Any:
        """
        :returns Any: the value of the characteristic.
        """
        raise NotImplementedError

    @abstractmethod
    def get_aspect(self) -> Aspect:
        """
        :returns Aspect: the aspect of the characteristic.
        """
        raise NotImplementedError
