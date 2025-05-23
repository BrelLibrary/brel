"""
This module contains the class for the Member report element in Brel.
Members are used to represent the possible values of an explicit dimension.

====================

- author: Robin Schmidiger
- version: 0.3
- date: 18 January 2023

====================
"""

from typing import Any, Dict
from brel import QName
from brel.reportelements import IReportElement
from brel.resource import BrelLabel


class Member(IReportElement):
    """
    Class representing a member in a BREL report. A member is a kind of report element that is used to represent the possible values of an explicit dimension.
    It implements the IReportElement interface.
    """

    def __init__(self, name: QName, id: str | None, labels: list[BrelLabel]):
        self.__name = name
        self.__id = id
        self.__labels = labels

    def get_name(self) -> QName:
        """
        :returns QName: the name of the member as a QName
        """
        return self.__name

    def get_id(self) -> str | None:
        """
        :returns str: the id of the member
        """
        return self.__id

    def get_labels(self) -> list[BrelLabel]:
        """
        :returns list[BrelLabel]: the labels of the member
        """
        return self.__labels

    def _add_label(self, label: BrelLabel):
        """
        Add a label to the member. This method is used by the parser and should not be used by the user.
        However, if you want to add a label to a member, you can use this method.
        :param label: the label to add to the member
        """
        self.__labels.append(label)

    def __str__(self) -> str:
        return self.__name.__str__()

    def convert_to_dict(self) -> Dict[str, Any]:
        """
        Convert the member to a dictionary.
        :returns dict: the member as a dictionary
        """
        return {
            "name": self.__name.prefix_local_name_notation(),
            "label": self.select_main_label().__str__(),
            "report_element_type": "member",
        }
