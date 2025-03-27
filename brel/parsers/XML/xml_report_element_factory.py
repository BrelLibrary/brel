"""
This module contains the XMLReportElementFactory class. It is responsible for creating report elements from lxml.etree._Element objects.

====================

- author: Robin Schmidiger
- version: 0.4
- date: 30 January 2024

====================
"""

from typing import cast, Tuple

import lxml
import lxml.etree

from brel import QName
from brel.reportelements import *
from brel.resource import BrelLabel


class XMLReportElementFactory:
    @staticmethod
    def create(
        xml_element: lxml.etree._Element,
        report_element_name: QName,
        labels: list[BrelLabel],
    ) -> Tuple[str | None, IReportElement] | None:
        """
        Creates a report element from an lxml.etree._Element.
        The kind of report element created depends on the structure of the lxml.etree._Element.
        :param xml_element: lxml.etree._Element. The lxml.etree._Element to create the report element from.
        :returns tuple[str, IReportElement] | None: The report element created and its ID.
        """

        is_abstract = xml_element.get("abstract", "false") == "true"

        is_item = "item" in xml_element.get("substitutionGroup", "")
        is_hypercube_item = "hypercubeItem" in xml_element.get("substitutionGroup", "")
        is_dimension_item = "dimensionItem" in xml_element.get("substitutionGroup", "")
        is_domain_item_type = "domainItemType" in xml_element.get("type", "")
        is_item = "item" in xml_element.get("substitutionGroup", "")

        is_line_items = "LineItems" in xml_element.get("name", "")

        id = xml_element.get("id", None)

        report_element: None | IReportElement = None

        if is_domain_item_type:
            report_element = Member(report_element_name, labels)
        # if not is_abstract and is_item:
        elif not is_abstract and is_item:
            report_element = Concept._from_xml(xml_element, report_element_name, labels)
        elif is_abstract and is_hypercube_item:
            report_element = Hypercube(report_element_name, labels)
        elif is_abstract and is_dimension_item:
            report_element = Dimension(report_element_name, labels)
        # elif is_abstract and is_domain_item_type and is_item:
        # report_element = Member(report_element_name, labels)
        elif is_abstract and is_line_items:
            report_element = LineItems(report_element_name, labels)
        elif is_abstract:
            report_element = Abstract(report_element_name, labels)
        else:
            return None

        report_element = cast(IReportElement, report_element)
        return id, report_element
