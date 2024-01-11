from __future__ import annotations
from enum import Enum

from brel import Fact, QName, QNameNSMap
from brel.characteristics import Aspect


class FilingFilterType(Enum):
    """Enum for the different types of filters"""

    CONCEPT = 1
    PERIOD = 2
    ENTITY = 3  # TODO: implement
    UNIT = 4  # TODO: implement
    ADDITIONAL_DIMENSION = 5
    BOOL_LIST = 6


class FilingFilter:
    """A wrapper class for filtering a list of facts according to a certain criteria"""

    def __init__(
        self, filter_list, filter_type: FilingFilterType, nsmap: QNameNSMap
    ) -> None:
        self.__filter_list = filter_list
        self.__filter_type = filter_type
        self.__nsmap = nsmap

    def get_filter_type(self) -> FilingFilterType:
        """Get the filter type"""
        return self.__filter_type

    def __eq__(self, other) -> "FilingFilter":  # type: ignore
        """Compare the values of the column with a string"""
        # force mypy to accept the comparison
        is_qname = QName.is_str_qname(other, self.__nsmap)
        if is_qname and self.__filter_type == FilingFilterType.CONCEPT:
            filter_list = [
                current_value == other for current_value in self.__filter_list
            ]
            return self.__class__(
                filter_list, FilingFilterType.BOOL_LIST, self.__nsmap
            )
        elif (
            is_qname
            and self.__filter_type == FilingFilterType.ADDITIONAL_DIMENSION
        ):
            filter_list = [
                current_value == other for current_value in self.__filter_list
            ]
            return self.__class__(
                filter_list, FilingFilterType.BOOL_LIST, self.__nsmap
            )
        else:
            # TODO: implement more than just concept filters
            raise NotImplementedError(
                "Only concept filters are implemented. The other filters are not implemented yet"
            )

    def __combine__piecewise(
        self, other: "FilingFilter" | list[bool], operator
    ) -> "FilingFilter":
        """
        Combine two filters with an 'operator' piecewise
        The other filter must be a list of bools or a FilingFilter of type BOOL_LIST
        """
        if isinstance(other, list):
            other_filter = other
        elif (
            isinstance(other, FilingFilter)
            and other.get_filter_type() == FilingFilterType.BOOL_LIST
        ):
            other_filter = other.get_filter_list()
        else:
            raise TypeError(
                "The other filter must be a list or a FilingFilter of type BOOL_LIST"
            )
        if len(other_filter) != len(self.__filter_list):
            raise ValueError(
                "The boolean list must have as many elements as there are facts"
            )

        filter_list = [
            operator(self.__filter_list[i], other_filter[i])
            for i in range(len(self.__filter_list))
        ]
        return self.__class__(
            filter_list, FilingFilterType.BOOL_LIST, self.__nsmap
        )

    def __and__(self, other: "FilingFilter" | list[bool]) -> "FilingFilter":
        """Combine two filters with an and"""
        return self.__combine__piecewise(other, lambda x, y: x and y)

    def __rand__(self, other: "FilingFilter" | list[bool]) -> "FilingFilter":
        """Combine two filters with an and"""
        return self.__and__(other)

    def __or__(self, other: "FilingFilter" | list[bool]) -> "FilingFilter":
        """Combine two filters with an or"""
        return self.__combine__piecewise(other, lambda x, y: x or y)

    def __ror__(self, other: "FilingFilter" | list[bool]) -> "FilingFilter":
        """Combine two filters with an or"""
        return self.__or__(other)

    def filter(self, other: list[Fact]) -> list[Fact]:
        """Apply the filter to a list of facts"""
        if len(other) != len(self.__filter_list):
            raise ValueError(
                "The boolean list must have as many elements as there are facts"
            )

        filter_list = [
            other[i]
            for i in range(len(self.__filter_list))
            if self.__filter_list[i]
        ]
        return filter_list

    def get_filter_list(self) -> list[bool]:
        """Get the filter list"""
        return self.__filter_list

    @classmethod
    def make_aspect_filter(
        cls, facts: list[Fact], aspect: Aspect, nsmap: QNameNSMap
    ) -> "FilingFilter":
        """Make a filter for a specific aspect"""
        # TODO: Implement more than just concept filters and additional dimension filters
        if aspect == Aspect.CONCEPT:
            filter_list = []
            for fact in facts:
                filter_list.append(
                    fact.get_context().get_characteristic(aspect).__str__()
                )
            return cls(filter_list, FilingFilterType.CONCEPT, nsmap)
        elif not aspect.is_core():
            filter_list = []
            for fact in facts:
                filter_list.append(
                    fact.get_context().get_characteristic(aspect).__str__()
                )
            return cls(
                filter_list, FilingFilterType.ADDITIONAL_DIMENSION, nsmap
            )
        else:
            raise NotImplementedError(
                "Only concept filters are implemented. The other filters are not implemented yet"
            )
