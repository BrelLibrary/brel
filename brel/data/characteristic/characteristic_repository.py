"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from typing import Callable, Type
from abc import ABC, abstractmethod
from brel.characteristics.i_characteristic import ICharacteristic


class CharacteristicRepository(ABC):
    @abstractmethod
    def get[T: ICharacteristic](self, id: str, characteristic_type: Type[T]) -> T:
        pass

    @abstractmethod
    def has(self, id: str, type: type[ICharacteristic]) -> bool:
        pass

    @abstractmethod
    def upsert(self, id: str, characteristic: ICharacteristic) -> None:
        pass

    def get_or_create[
        T: ICharacteristic
    ](self, id: str, characteristic_type: Type[T], factory: Callable[[], T]) -> T:
        if not self.has(id, characteristic_type):
            characteristic = factory()
            self.upsert(id, characteristic)
        return self.get(id, characteristic_type)
