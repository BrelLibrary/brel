from typing import Optional
from brel.formula.filters.filter import Filter
from brel.formula.filters.period.period_date_time_filter_type import (
    PeriodDateTimeFilterType,
)
from brel.formula.xpath_expression import XPathExpression


class PeriodDateTimeFilter(Filter):
    def __init__(
        self,
        date: XPathExpression,
        time: Optional[XPathExpression],
        type: PeriodDateTimeFilterType,
        label: Optional[str],
        id: Optional[str],
    ):
        self.date = date
        self.time = time
        self.type = type
        super().__init__(label, id)

    def get_date_expression(self) -> XPathExpression:
        return self.date

    def get_time_expression(self) -> Optional[XPathExpression]:
        return self.time

    def get_type(self) -> PeriodDateTimeFilterType:
        return self.type
