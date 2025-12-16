from typing import List, Optional
from brel.formula.filters.filter import Filter
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class ConceptNameFilter(Filter):
    def __init__(self, label: Optional[str], id: Optional[str]) -> None:
        self.qnames: List[QName] = []
        self.qname_expressions: List[XPathExpression] = []
        super().__init__(label, id)

    def add_qname(self, qname: QName) -> None:
        self.qnames.append(qname)

    def add_qname_expression(self, qname_expression: XPathExpression) -> None:
        self.qname_expressions.append(qname_expression)

    def get_qnames(self) -> List[QName]:
        return self.qnames

    def get_qname_expressions(self) -> List[XPathExpression]:
        return self.qname_expressions
