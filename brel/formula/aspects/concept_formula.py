from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class ConceptFormula(AspectFormula):
    def __init__(self, qname_or_expression: QName | XPathExpression) -> None:
        self.__qname_or_expression: QName | XPathExpression = qname_or_expression
        super().__init__(Aspect.CONCEPT)

    def get_qname(self) -> Optional[QName]:
        if isinstance(self.__qname_or_expression, QName):
            return self.__qname_or_expression
        return None

    def get_expression(self) -> Optional[XPathExpression]:
        if isinstance(self.__qname_or_expression, XPathExpression):
            return self.__qname_or_expression
        return None
