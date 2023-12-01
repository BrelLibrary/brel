import lxml
import lxml.etree

from pybr import QName, BrelLabel
from pybr.reportelements import *

class XMLReportElementFactory():
    @staticmethod
    def create(xml_element: lxml.etree._Element, report_element_name: QName, labels: list[BrelLabel]) -> IReportElement | None:
        """
        Creates a report element from an lxml.etree._Element.
        The kind of report element created depends on the structure of the lxml.etree._Element.
        @param xml_element: lxml.etree._Element. The lxml.etree._Element to create the report element from.
        @return: IReportElement. The report element created. This is one of the following: PyBRConcept, PyBRAbstract, PyBRHypercube, PyBRMember, PyBRLineItems, PyBRDimension.
        """

        # if there is no "abstract" attribute, then it is a concept
        # if there is an "abstract" attribute and the substitutionGroup attribute is "xbrldt:hypercubeItem", then it is a HyperCube
        # if there is an "abstract" attribute and the substitutionGroup attribute is "xbrldt:dimensionItem", then it is a Dimension
        # if there is an "abstract" attribute and the type attribute is "dtr-types1:domainItemType", then it is a Member
        # else it is an Abstract
        # TODO: Think about how to differentiate between LineItems and Abstracts. For now, we just return an Abstract.
        # TODO: check prefixes, not just local_names
        is_abstract = xml_element.get("abstract", "false") == "true"

        is_item = "item" in xml_element.get("substitutionGroup", "")
        is_hypercube_item = "hypercubeItem" in xml_element.get("substitutionGroup", "")
        is_dimension_item = "dimensionItem" in xml_element.get("substitutionGroup", "")
        is_domain_item_type = "domainItemType" in xml_element.get("type", "")
        is_item = "item" in xml_element.get("substitutionGroup", "")


        # TODO: think if this is robust enough. maybe I cannot just toss the namespace away
        if not is_abstract and is_item:
            return PyBRConcept.from_xml(xml_element, report_element_name, labels)
        elif is_abstract and is_hypercube_item:
            return PyBRHypercube(report_element_name, labels)
        elif is_abstract and is_dimension_item:
            return PyBRDimension(report_element_name, labels)
        elif is_abstract and is_domain_item_type and is_item:
            return PyBRMember(report_element_name, labels)
        elif is_abstract:
            # print(report_element_name, "is an abstract")
            return PyBRAbstract(report_element_name, labels)
        else:
            return None