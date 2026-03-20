from typing import Optional
from brel.formula.filters.filter import Filter


class ForeverFilter(Filter):
    def __init__(self, label: Optional[str], id: Optional[str]) -> None:
        super().__init__(label, id)
