from typing import Optional
from brel.characteristics.brel_aspect import Aspect
from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.xpath_expression import XPathExpression


class PeriodDurationFormula(AspectFormula):
    def __init__(
        self,
        start_expression: Optional[XPathExpression],
        end_expression: Optional[XPathExpression],
    ) -> None:
        self.start_expression = start_expression
        self.end_expression = end_expression

        super().__init__(Aspect.PERIOD)

    def get_start_expression(self) -> Optional[XPathExpression]:
        return self.start_expression

    def get_end_expression(self) -> Optional[XPathExpression]:
        return self.end_expression
