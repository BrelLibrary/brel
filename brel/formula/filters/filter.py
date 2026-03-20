from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.qnames.qname import QName


class Filter:
    def __init__(self, label: Optional[str], id: Optional[str]) -> None:
        self.label = label
        self.id = id
        self.is_complement = False

    def set_is_complement(self, is_complement: bool) -> None:
        self.is_complement = is_complement

    def get_label(self) -> Optional[str]:
        return self.label

    def get_id(self) -> Optional[str]:
        return self.id

    def get_is_complement(self) -> bool:
        return self.is_complement
