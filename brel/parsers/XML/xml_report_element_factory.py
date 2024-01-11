"""
This module contains the XMLReportElementFactory class. It is responsible for creating report elements from lxml.etree._Element objects.

@author: Robin Schmidiger
@version: 0.0.2
@date: 18 December 2023
"""

import lxml
import lxml.etree

from brel import QName, BrelLabel
from brel.reportelements import *

from typing import cast


class XMLReportElementFactory:
    @staticmethod
    def create(
        xml_element: lxml.etree._Element,
        report_element_name: QName,
        labels: list[BrelLabel],
    ) -> tuple[str | None, IReportElement] | None:
        """
        Creates a report element from an lxml.etree._Element.
        The kind of report element created depends on the structure of the lxml.etree._Element.
        @param xml_element: lxml.etree._Element. The lxml.etree._Element to create the report element from.
        @return: tuple[str, IReportElement] | None. The report element created and its ID.
        # @return: IReportElement. The report element created. This is one of the following: Concept, Abstract, Hypercube, Member, LineItems, Dimension.
        """

        # if there is no "abstract" attribute, then it is a concept
        # if there is an "abstract" attribute and the substitutionGroup attribute is "xbrldt:hypercubeItem", then it is a HyperCube
        # if there is an "abstract" attribute and the substitutionGroup attribute is "xbrldt:dimensionItem", then it is a Dimension
        # if there is an "abstract" attribute and the type attribute is "dtr-types1:domainItemType", then it is a Member
        # else it is an Abstract
        # TODO: Think about how to differentiate between LineItems and Abstracts. For now, we just return an Abstract.

        # if xml_element.get("abstract", None) is None:
        #     return None

        is_abstract = xml_element.get("abstract", "false") == "true"

        is_item = "item" in xml_element.get("substitutionGroup", "")
        is_hypercube_item = "hypercubeItem" in xml_element.get(
            "substitutionGroup", ""
        )
        is_dimension_item = "dimensionItem" in xml_element.get(
            "substitutionGroup", ""
        )
        is_domain_item_type = "domainItemType" in xml_element.get("type", "")
        is_item = "item" in xml_element.get("substitutionGroup", "")

        id = xml_element.get("id", None)

        # TODO: think if this is robust enough. maybe I cannot just toss the namespace away
        report_element: None | IReportElement = None

        if not is_abstract and is_item:
            report_element = Concept._from_xml(
                xml_element, report_element_name, labels
            )
        elif is_abstract and is_hypercube_item:
            report_element = Hypercube(report_element_name, labels)
        elif is_abstract and is_dimension_item:
            report_element = Dimension(report_element_name, labels)
        elif is_abstract and is_domain_item_type and is_item:
            report_element = Member(report_element_name, labels)
        elif is_abstract:
            report_element = Abstract(report_element_name, labels)
        else:
            return None

        report_element = cast(IReportElement, report_element)
        return id, report_element
