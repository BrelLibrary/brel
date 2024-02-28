"""
This module contains the interface for all report elements.
Report elements are the building blocks of a report and are used by a lot of other classes.
Therefore, it is important to have a common interface for all report elements.

Report have a unique name and can have multiple human readable labels representing the same name.
Depending on the kind of report element, there might be more information available.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 21 January 2024

====================
"""

from abc import ABC, abstractmethod

from brel import QName
from brel.resource import BrelLabel


class IReportElement(ABC):
    """
    Interface for all report elements.
    Each report element must have a name and can have multiple labels.
    """

    # first class citizens
    @abstractmethod
    def get_name(self) -> QName:  # pragma: no cover
        """
        Get the name of the report element.
        :returns: QName containing the name of the report element
        """
        raise NotImplementedError

    @abstractmethod
    def get_labels(self) -> list[BrelLabel]:  # pragma: no cover
        """
        Get all labels of the report element.
        :returns list[Label]: containing the labels of the report element
        """
        raise NotImplementedError

    @abstractmethod
    def _add_label(self, label: BrelLabel):  # pragma: no cover
        raise NotImplementedError

    # second class citizens
    def has_label_with_role(self, label_role: str) -> bool:
        """
        Check if the report element has a label with the given role.
        :param label_role: the role of the label to check
        :returns bool: True if the report element has a label with the given role, False otherwise
        """
        return any(label.get_label_role() == label_role for label in self.get_labels())

    def has_label_with_language(self, language: str) -> bool:
        """
        Check if the report element has a label with the given language.
        :param language: the language of the label to check
        :returns bool: True if the report element has a label with the given language, False otherwise
        """
        return any(label.get_language() == language for label in self.get_labels())
