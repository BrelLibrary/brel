"""
====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 May 2025

====================
"""
from abc import abstractmethod, ABC

from brel.characteristics.brel_aspect import Aspect
from brel.qnames.qname import QName


class AspectRepository(ABC):
    @abstractmethod
    def get(self, name: str) -> Aspect:
        raise NotImplementedError()

    def get_by_qname(self, qname: QName) -> Aspect:
        return self.get(qname.prefix_local_name_notation())

    @abstractmethod
    def has(self, name: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def upsert(self, aspect: Aspect) -> None:
        raise NotImplementedError()
