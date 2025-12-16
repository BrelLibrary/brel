from typing import Optional
from brel.formula.filters.filter import Filter
from brel.formula.xpath_expression import XPathExpression


class PeriodFilter(Filter):
    def __init__(
        self, test_expression: XPathExpression, label: Optional[str], id: Optional[str]
    ):
        self.test_expression = test_expression
        super().__init__(label, id)

    def get_test_expression(self) -> XPathExpression:
        return self.test_expression
