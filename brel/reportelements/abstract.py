"""
This module contains the Abstract class. An abstract a kind of report element that is used to group other report elements.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 30 October 2023

====================
"""

from typing import Any, Dict
from brel import QName
from brel.reportelements import IReportElement
from brel.resource import BrelLabel


class Abstract(IReportElement):
    """
    Class representing an abstract in a BREL report. An abstract is a kind of report element that is used to group other report elements.
    They are often used in presentation networks to build a hierarchy of concepts.

    The Abstract class implements the IReportElement interface.
    """

    def __init__(self, qname: QName, id: str | None, labels: list[BrelLabel]) -> None:
        self.__qname = qname
        self.__id = id
        self.__labels = labels

    def get_name(self) -> QName:
        """
        Get the name of the abstract element.
        :returns QName: containing the name of the abstract element
        """
        return self.__qname

    def get_id(self) -> str | None:
        """
        Get the id of the abstract element.
        :returns str: containing the id of the abstract element
        """
        return self.__id

    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the abstract element.
        :returns list[Label]: contains the labels of the abstract element
        """
        return self.__labels

    def _add_label(self, label: BrelLabel):
        """
        Add a label to the abstract element.
        :param label: the label to add to the abstract element
        """
        self.__labels.append(label)

    def __str__(self) -> str:
        return self.__qname.__str__()

    def convert_to_dict(self) -> Dict[str, Any]:
        """
        Convert the abstract element to a dictionary.
        :returns dict: the abstract element as a dictionary
        """
        return {
            "name": self.__qname.prefix_local_name_notation(),
            "label": self.select_main_label().__str__(),
            "report_element_type": "abstract",
        }
