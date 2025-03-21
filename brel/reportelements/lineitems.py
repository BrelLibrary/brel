"""
This module contains the LineItems class.

=================

- author: Robin Schmidiger
- version: 0.2
- date: 18 January 2024

=================
"""

from brel import QName
from brel.reportelements import IReportElement
from brel.resource import BrelLabel


class LineItems(IReportElement):
    def __init__(self, name: QName, labels: list[BrelLabel]):
        self.__name = name
        self.__labels = labels

    def get_name(self) -> QName:
        """
        :returns QName: the name of the line items as a QName
        """
        return self.__name

    def get_labels(self) -> list[BrelLabel]:
        """
        :returns list[BrelLabel]: the labels of the line items
        """
        return self.__labels

    def _add_label(self, label: BrelLabel):
        """
        Add a label to the line items. This method is used by the parser and should not be used by the user.
        However, if you want to add a label to a line items, you can use this method.
        :param label: the label to add to the line items
        """
        self.__labels.append(label)

    def __str__(self) -> str:
        """
        :returns str: the name of the line items as a string
        """
        return self.__name.__str__()

    def convert_to_dict(self) -> dict:
        """
        Convert the line items to a dictionary.
        :returns dict: the line items as a dictionary
        """
        return {
            "name": self.__name.get(),
            "label": self.select_main_label().__str__(),
            "report_element_type": "line item",
        }
