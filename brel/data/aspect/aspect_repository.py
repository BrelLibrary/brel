"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 10 April 2025

====================
"""
from abc import abstractmethod, ABC

from brel.characteristics.brel_aspect import Aspect
from brel.qname import QName


class AspectRepository(ABC):
    @abstractmethod
    def get(self, name: str) -> Aspect:
        raise NotImplementedError()

    def get_by_qname(self, qname: QName) -> Aspect:
        return self.get(qname.get())

    @abstractmethod
    def has(self, name: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def upsert(self, aspect: Aspect) -> None:
        raise NotImplementedError()
