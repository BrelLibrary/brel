"""
This module contains the Concept class. A Concept is a data item that can be reported on.
Concepts in BREL reports are the same as concepts in XBRL reports.
For more information on concepts, see the [**XBRL 2.1 specification**](https://specifications.xbrl.org/work-product-index-group-base-spec-base-spec.html)

====================

- author: Robin Schmidiger
- version: 0.5
- date: 04 December 2023

====================
"""

from typing import Any, Dict, List, Optional
import lxml
import lxml.etree

from brel import QName
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode
from brel.reportelements import IReportElement
from brel.resource import BrelLabel
from brel.services.translation.translation_service import TranslationService


class Concept(IReportElement):
    """
    Class representing a concept in a BREL report. A concept is a data item that can be reported on.
    Concepts in BREL reports are the same as concepts in XBRL reports.
    For more information on concepts, see the XBRL 2.1 specification.
    A short summary of the most important attributes of a concept:

    - It is defined in the XBRL taxonomy. So in the .xsd files in the DTS.
    - It has a name, which is a QName. This has to be unique in the DTS.
    - It has a data type, which is a QName.
    - It has a period type, which can be either instant or duration.
    - (optional) It has a balance type, which can be either credit or debit.
    - (optional) It can be nillable, which is either true or false. If the attribute is not present, it defaults to false.

    """

    def __init__(
        self,
        name: QName,
        id: str | None,
        labels: list[BrelLabel],
        period_type: str,
        balance_type: str | None,
        nillable: bool,
        data_type: str,
    ) -> None:
        self.__name: QName = name
        self.__id: str | None = id
        self.__labels: list[BrelLabel] = labels
        self.__period_type: str = period_type
        self.__balance_type: str | None = balance_type
        self.__nillable: bool = nillable
        self.__data_type: str = data_type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Concept):
            return False

        # there can only be one concept with a given name in a DTS
        return self.__name == other.__name

    def get_name(self) -> QName:
        """
        Get the name of the concept.
        :returns QName: the QName of the concept
        """
        return self.__name

    def get_id(self) -> str | None:
        """
        Get the id of the concept.
        :returns str|None: the id of the concept
        """
        return self.__id

    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the concept.
        :returns list[Label]: all labels of the concept
        """
        return self.__labels

    def _add_label(self, label: BrelLabel) -> None:
        """
        Add a label to the concept.
        :param label: the label to add to the concept
        """
        self.__labels.append(label)

    def get_period_type(self) -> str:
        """
        Get the period type of the concept.
        :returns str: the period type of the concept
        """
        return self.__period_type

    def get_data_type(self) -> str:
        """
        Get the data type of the concept.
        :returns str: the data type of the concept
        """
        return self.__data_type

    def get_balance_type(self) -> str | None:
        """
        Get the balance type of the concept.
        :returns str|None: the balance type of the concept. None if the concept has no balance type.
        """
        return self.__balance_type

    def is_nillable(self) -> bool:
        """
        Check if the concept is nillable.
        :returns bool: True 'IFF' the concept is nillable, False otherwise
        """
        return self.__nillable

    @classmethod
    def _from_xml(
        cls,
        xml_element: lxml.etree._Element,
        id: str | None,
        concept_qname: QName,
        labels: list[BrelLabel],
        error_repository: ErrorRepository,
    ) -> Optional["Concept"]:
        """
        Create a Concept from an lxml.etree._Element.
        :param xml_element: lxml.etree._Element. The lxml.etree._Element to create the Concept from.
        :param concept_qname: QName. The QName of the concept.
        :returns Concept: The Concept created from the lxml.etree._Element.
        """
        nsmap = {"xbrli": "http://www.xbrl.org/2003/instance"}

        # get the period type of the concept
        period_type = xml_element.get(f"{{{nsmap['xbrli']}}}periodType", None)
        # according to the XBRL 2.1 specification, the period type can be either instant or duration
        possible_period_types = ["instant", "duration"]
        if period_type not in possible_period_types:
            error_repository.insert(
                ErrorCode.INVALID_CONCEPT_PERIOD_TYPE,
                xml_element,
                concept_name=concept_qname.get_local_name(),
                period_type=period_type,
            )

            return None

        # get the balance type of the concept
        balance_type = xml_element.get(f"{{{nsmap['xbrli']}}}balance", None)
        # According to the XBRL 2.1 specification, the balance type can be either credit or debit.
        # The "None" is because the "balance" attribute is optional and only applies to monetary items.
        possible_balance_types = ["credit", "debit", None]
        if balance_type not in possible_balance_types:
            error_repository.insert(
                ErrorCode.INVALID_CONCEPT_BALANCE_TYPE,
                xml_element,
                concept_name=concept_qname.get_local_name(),
                balance_type=balance_type,
            )

            return None

        # get if the concept is nillable
        xml_nillable = xml_element.get("nillable", None)
        # According to the XBRL 2.1 specification, the nillable attribute can be either true or false.
        # It is optional (thus the "None" in possible_nillable_values), and defaults to false.
        possible_nillable_values = ["true", "false", None]
        if xml_nillable not in possible_nillable_values:
            error_repository.insert(
                ErrorCode.INVALID_CONCEPT_NILLABLE_VALUE,
                xml_element,
                concept_name=concept_qname.get_local_name(),
                nillable_value=xml_nillable,
            )

            return None
        else:
            nillable = xml_nillable == "true"

        # get the data type of the concept
        data_type = xml_element.get("type", None)
        if data_type is None:
            error_repository.insert(
                ErrorCode.MISSING_CONCEPT_DATA_TYPE,
                xml_element,
                concept_name=concept_qname.get_local_name(),
            )

            return None

        return cls(
            concept_qname,
            id,
            labels,
            period_type,
            balance_type,
            nillable,
            data_type,
        )

    def __str__(self) -> str:
        return self.__name.__str__()

    def convert_to_dict(
        self,
        languages: Optional[List[str]] = None,
        translation_service: Optional[TranslationService] = None,
    ) -> Dict[str, Any]:
        """
        Convert the concept to a dictionary.
        :returns dict: the concept as a dictionary
        """
        if not languages or not translation_service:
            return {
                "name": self.__name.prefix_local_name_notation(),
                "label": self.select_main_label().__str__(),
                "report-element-type": "concept",
                "period-type": self.__period_type,
                "balance-type": self.__balance_type,
                "nillable": self.__nillable,
                "data-type": self.__data_type,
            }
        name_literal = translation_service.get("literal:name", languages)

        label_literal = translation_service.get("literal:label", languages)
        label = translation_service.get_from_labels(
            self.get_labels(), languages, self.select_main_label().__str__()
        )

        report_element_type_literal = translation_service.get(
            "literal:report-element-type",
            languages,
        )
        concept_literal = translation_service.get("report-element:concept", languages)

        period_type_literal = translation_service.get("literal:period-type", languages)
        period_type = translation_service.get(
            "period-type:" + self.__period_type, languages
        )

        balance_type_literal = translation_service.get(
            "literal:balance-type", languages
        )
        if self.__balance_type is not None:
            balance_type = translation_service.get(
                "balance-type:" + self.__balance_type, languages
            )
        else:
            balance_type = translation_service.get("literal:none", languages)

        nillable_literal = translation_service.get("literal:nillable", languages)
        nillable = translation_service.get(
            "boolean:" + str(self.__nillable).lower(), languages
        )

        data_type_literal = translation_service.get("literal:data-type", languages)
        data_type = translation_service.get(
            "data-type:" + self.__data_type.split(":")[-1], languages
        )

        return {
            name_literal: self.__name.prefix_local_name_notation(),
            label_literal: label,
            report_element_type_literal: concept_literal,
            period_type_literal: period_type,
            balance_type_literal: balance_type,
            nillable_literal: nillable,
            data_type_literal: data_type,
        }
