"""
This module contains the Abstract class. An abstract a kind of report element that is used to group other report elements.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 30 October 2023

====================
"""

from typing import Any, Dict, List, Optional
from brel import QName
from brel.reportelements import IReportElement
from brel.resource import BrelLabel
from brel.services.translation.translation_service import TranslationService


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

    def convert_to_dict(
        self,
        languages: Optional[List[str]] = None,
        translation_service: Optional[TranslationService] = None,
    ) -> Dict[str, Any]:
        """
        Convert the abstract element to a dictionary.
        :returns dict: the abstract element as a dictionary
        """
        if not languages or not translation_service:
            return {
                "name": self.__qname.prefix_local_name_notation(),
                "label": self.select_main_label().__str__(),
                "report-element-type": "abstract",
            }

        name_literal = translation_service.get("literal:name", languages)
        label_literal = translation_service.get("literal:label", languages)
        report_element_type_literal = translation_service.get(
            "literal:report-element-type", languages
        )
        abstract_literal = translation_service.get("report-element:abstract", languages)

        label = translation_service.get_from_labels(
            self.get_labels(), languages, self.select_main_label().__str__()
        )

        return {
            name_literal: self.__qname.prefix_local_name_notation(),
            label_literal: label,
            report_element_type_literal: abstract_literal,
        }
