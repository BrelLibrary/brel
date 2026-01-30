from typing import Optional
from brel.formula.filters.dimension.member_axis import MemberAxis
from brel.formula.xpath_expression import XPathExpression
from brel.qnames.qname import QName


class ExplicitDimensionFilterMember:
    def __init__(self, member: QName | XPathExpression) -> None:
        self.__member: QName | XPathExpression = member
        self.__linkrole: Optional[str] = None
        self.__arcrole: Optional[str] = None
        self.__axis: MemberAxis = MemberAxis.UNSPECIFIED

    def get_member(self) -> QName | XPathExpression:
        return self.__member

    def get_linkrole(self) -> Optional[str]:
        return self.__linkrole

    def get_arcrole(self) -> Optional[str]:
        return self.__arcrole

    def get_axis(self) -> MemberAxis:
        return self.__axis

    def set_linkrole(self, linkrole: str) -> None:
        self.__linkrole = linkrole

    def set_arcrole(self, arcrole: str) -> None:
        self.__arcrole = arcrole

    def set_axis(self, axis: MemberAxis) -> None:
        self.__axis = axis
