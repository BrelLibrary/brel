"""
This module contains the Abstract class. An abstract a kind of report element that is used to group other report elements.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 30 October 2023

====================
"""

from brel import QName, BrelLabel
from brel.reportelements import IReportElement


class Abstract(IReportElement):
    """
    Class representing an abstract in a BREL report. An abstract is a kind of report element that is used to group other report elements.
    They are often used in presentation networks to build a hierarchy of concepts.

    The Abstract class implements the IReportElement interface.
    """

    def __init__(self, qname: QName, labels: list[BrelLabel]) -> None:
        self.__qname = qname
        self.__labels = labels

    def get_name(self) -> QName:
        """
        Get the name of the abstract element.
        :returns QName: containing the name of the abstract element
        """
        return self.__qname

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
