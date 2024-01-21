"""
This module contains the Dimension class. A dimension is a kind of report element that is used to present additional aspects for the context of a fact.

Facts in Brel can already be viewed as a form of hypercube. Dimensions build on top of that and allow for custom dimensions to be added to the hypercube besides the already existing ones.
The already existing dimensions are the core aspects of a fact, namely the period, the entity, the unit and the concept.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 30 October 2023

====================
"""

from brel import QName
from brel.reportelements import IReportElement
from brel.resource import BrelLabel


class Dimension(IReportElement):
    """
    Class representing a dimension in a BREL report. A dimension is a kind of report element that is used to present additional aspects for the context of a fact.

    All dimensions are either explicit or typed.
    A new dimension is explicit by default.
    If you want to make a dimension typed, you have to call `make_typed(dim_type: QName)` on it.
    """

    def __init__(self, name: QName, labels: list[BrelLabel]) -> None:
        self.__name = name
        self.__labels = labels
        self.__type: QName | None = None

    def get_name(self) -> QName:
        """
        Get the name of the dimension.
        :returns QName: the name of the dimension as a QName
        """
        return self.__name

    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the dimension.
        :returns list[Label]: all labels of the dimension
        """
        return self.__labels

    def _add_label(self, label: BrelLabel):
        """
        Add a label to the dimension.
        :param label: the label to add to the dimension
        """
        self.__labels.append(label)

    def is_explicit(self) -> bool:
        """
        Check if the dimension is explicit.
        Use the `make_typed(dim_type: QName)` method to make a dimension typed.
        :returns bool: True 'IFF' the dimension is explicit, False otherwise
        """
        return self.__type is None

    def get_type(self) -> QName:
        """
        Get the type of the dimension.
        :returns QName: type of the dimension
        :raises ValueError: if the dimension is explicit and has no type
        Use `is_explicit()` to check if the dimension is explicit.
        """
        if self.__type is None:
            raise ValueError("Dimension is explicit and has no type")

        return self.__type

    def make_typed(self, dim_type: QName):
        """
        Turn the dimension into a typed dimension.
        :param dim_type: the type of the dimension. Has to be a QName
        """
        self.__type = dim_type

    def __str__(self) -> str:
        return self.__name.__str__()
