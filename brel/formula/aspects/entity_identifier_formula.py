from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class EntityIdentifierFormula(AspectFormula):
    def __init__(
        self, scheme: Optional[XPathExpression], value: Optional[XPathExpression]
    ) -> None:
        self.scheme = scheme
        self.value = value
        super().__init__(Aspect.ENTITY)

    def get_scheme(self) -> Optional[XPathExpression]:
        return self.scheme

    def get_value(self) -> Optional[XPathExpression]:
        return self.value
