from typing import List, Optional
from brel.formula.filters.dimension.dimension_filter import DimensionFilter
from brel.formula.filters.dimension.explicit_dimension_filter_member import (
    ExplicitDimensionFilterMember,
)
from brel.formula.filters.filter import Filter
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class ExplicitDimensionFilter(DimensionFilter):
    def __init__(
        self,
        dimension: QName | XPathExpression,
        label: Optional[str],
        id: Optional[str],
    ):
        self.allowed_members: List[ExplicitDimensionFilterMember] = []
        super().__init__(dimension, label, id)

    def add_allowed_member(self, member: ExplicitDimensionFilterMember) -> None:
        self.allowed_members.append(member)

    def get_allowed_members(self) -> List[ExplicitDimensionFilterMember]:
        return self.allowed_members
