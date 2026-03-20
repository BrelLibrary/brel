from typing import Optional
from brel.formula.filters.dimension.dimension_filter import DimensionFilter
from brel.formula.filters.dimension.explicit_dimension_filter_member import (
    ExplicitDimensionFilterMember,
)
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class TypedDimensionFilter(DimensionFilter):
    def __init__(
        self,
        dimension: QName | XPathExpression,
        test: Optional[XPathExpression],
        label: Optional[str],
        id: Optional[str],
    ) -> None:
        self.test = test
        super().__init__(dimension, label, id)

    def get_test_expression(self) -> Optional[XPathExpression]:
        return self.test
