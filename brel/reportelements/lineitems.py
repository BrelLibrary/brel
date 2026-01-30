"""
This module contains the LineItems class.

=================

- author: Robin Schmidiger
- version: 0.2
- date: 18 January 2024

=================
"""

from typing import Dict, Any, List, Optional
from brel import QName
from brel.reportelements import IReportElement
from brel.resource import BrelLabel
from brel.services.translation.translation_service import TranslationService


class LineItems(IReportElement):
    def __init__(self, name: QName, id: str | None, labels: list[BrelLabel]):
        self.__name = name
        self.__id = id
        self.__labels = labels

    def get_name(self) -> QName:
        """
        :returns QName: the name of the line items as a QName
        """
        return self.__name

    def get_id(self) -> str | None:
        """
        :returns str: the id of the line items
        """
        return self.__id

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

    def convert_to_dict(
        self,
        languages: Optional[List[str]] = None,
        translation_service: Optional[TranslationService] = None,
    ) -> Dict[str, Any]:
        """
        Convert the line items to a dictionary.
        :returns dict: the line items as a dictionary
        """
        if not languages or not translation_service:
            return {
                "name": self.__name.prefix_local_name_notation(),
                "label": self.select_main_label().__str__(),
                "report-element-type": "line item",
            }

        name_literal = translation_service.get("literal:name", languages)
        label_literal = translation_service.get("literal:label", languages)
        report_element_type_literal = translation_service.get(
            "literal:report-element-type", languages
        )
        line_items_literal = translation_service.get(
            "report-element:line-items", languages
        )

        label = translation_service.get_from_labels(
            self.get_labels(), languages, self.select_main_label().__str__()
        )

        return {
            name_literal: self.__name.prefix_local_name_notation(),
            label_literal: label,
            report_element_type_literal: line_items_literal,
        }
