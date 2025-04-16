"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 11 April 2025

====================
"""

from typing import Tuple, Dict, Type

from brel.characteristics.i_characteristic import ICharacteristic
from brel.data.characteristic.characteristic_repository import CharacteristicRepository


class InMemoryCharacteristicRepository(CharacteristicRepository):
    def __init__(self) -> None:
        self.__characteristics: Dict[
            Tuple[str, Type[ICharacteristic]], ICharacteristic
        ] = {}

    def get[T: ICharacteristic](self, id: str, characteristic_type: Type[T]) -> T:
        characteristic = self.__characteristics.get((id, characteristic_type))
        if isinstance(characteristic, characteristic_type):
            return characteristic
        else:
            raise ValueError(
                f"Characteristic {id} is not of type {characteristic_type}. It is of type {type(characteristic)}"
            )

    def has(self, id: str, type: type[ICharacteristic]) -> bool:
        return (id, type) in self.__characteristics

    def upsert(self, id: str, characteristic: ICharacteristic) -> None:
        self.__characteristics[(id, type(characteristic))] = characteristic
