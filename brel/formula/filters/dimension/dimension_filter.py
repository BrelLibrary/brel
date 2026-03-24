from typing import List, Optional
from brel.formula.filters.dimension.explicit_dimension_filter_member import (
    ExplicitDimensionFilterMember,
)
from brel.formula.filters.filter import Filter
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class DimensionFilter(Filter):
    def __init__(
        self,
        dimension: QName | XPathExpression,
        label: Optional[str],
        id: Optional[str],
    ) -> None:
        self.dimension: QName | XPathExpression = dimension
        super().__init__(label, id)

    def get_dimension(self) -> QName | XPathExpression:
        return self.dimension
