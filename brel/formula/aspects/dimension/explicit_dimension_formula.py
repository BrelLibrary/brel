from typing import Optional
from brel.formula.aspects.dimension.dimension_formula import DimensionFormula
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class ExplicitDimensionFormula(DimensionFormula):
    def __init__(
        self, dimension: QName, member: Optional[QName | XPathExpression]
    ) -> None:
        self.member = member
        self.should_be_ommited = member is None
        super().__init__(dimension)

    def get_member(self) -> Optional[QName | XPathExpression]:
        return self.member

    def get_should_be_ommited(self) -> bool:
        return self.should_be_ommited
