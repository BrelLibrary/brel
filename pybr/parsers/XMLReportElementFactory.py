import lxml
import lxml.etree
from pybr import QName
from pybr.reportelements import *

class XMLReportElementFactory():
    def create(self, xml_element: lxml.etree._Element, report_element_name: QName) -> IReportElement:
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
        # TODO: Implement Labels
        has_abstract = xml_element.get("abstract", None) is not None

        # TODO: think if this is robust enough. maybe I cannot just toss the namespace away
        if not has_abstract:
            return PyBRConcept.from_xml(xml_element, report_element_name)
        elif "hypercubeItem" in xml_element.get("substitutionGroup", ""):
            return PyBRHypercube(report_element_name, [])
        elif "dimensionItem" in xml_element.get("substitutionGroup", ""):
            return PyBRDimension(report_element_name, [])
        elif "domainItemType" in xml_element.get("type", ""):
            return PyBRMember(report_element_name, [])
        else:
            # print(report_element_name, "is an abstract")
            return PyBRAbstract(report_element_name, [])