from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class PeriodForeverFormula(AspectFormula):
    def __init__(self) -> None:
        super().__init__(Aspect.PERIOD)
