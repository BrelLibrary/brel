from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.xpath_expression import XPathExpression


class PeriodInstantFormula(AspectFormula):
    def __init__(self, instant_expression: Optional[XPathExpression]) -> None:
        self.instant_expression = instant_expression
        super().__init__(Aspect.PERIOD)

    def get_instant_expression(self) -> Optional[XPathExpression]:
        return self.instant_expression
