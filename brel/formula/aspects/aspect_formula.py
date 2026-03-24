from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.qnames.qname import QName


class AspectFormula:
    def __init__(self, aspect: Aspect) -> None:
        self.aspect: Aspect = aspect

    def get_aspect(self) -> Aspect:
        return self.aspect
