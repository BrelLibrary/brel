"""
This module contains the function to parse the report elements from the xbrl instance.
It parses XBRL in the XML syntax.

@author: Robin Schmidiger
@version: 0.4
@date: 04 January 2024
"""

import lxml.etree
from ..dts import IFileManager
from brel.reportelements import IReportElement, Dimension
from brel import QName, QNameNSMap

from .xml_report_element_factory import XMLReportElementFactory
from brel.parsers.utils import get_str


def parse_report_elements_xml(
    file_manager: IFileManager,
    etrees: list[lxml.etree._ElementTree],
    qname_nsmap: QNameNSMap,
) -> tuple[dict[QName, IReportElement], dict[str, IReportElement]]:
    """
    Parse the concepts.
    @param file_manager: The file manager that contains the xbrl instance and the schemas.
    @param qname_nsmap: The QNameNSMap that contains all the namespaces used in the filing.
    @return: A dictionary mapping the QName to the report element. Contains all the report elements in the filing, even those that are not reported against.
    @return: A dictionary mapping the id of the xml element to the report element. This is useful for resolving hrefs.
    """

    report_elements: dict[QName, IReportElement] = {}
    id_to_report_element: dict[str, IReportElement] = {}

    for etree in etrees:
        # reportelem_url = etree.getroot().get("targetNamespace", None)
        # if reportelem_url is None:
        #     raise ValueError(
        #         f"the root element of the schema {etree} does not have a targetNamespace attribute"
        #     )
        reportelem_url = get_str(etree.getroot(), "targetNamespace")

        # get all the concept xml elements in the schema that have an attribute name
        re_xmls = etree.findall(".//{*}element[@name]", namespaces=None)
        for re_xml in re_xmls:
            # reportelem_name = re_xml.get("name")
            # if reportelem_name is None:
            #     raise ValueError(f"the element {re_xml} does not have a name attribute")
            reportelem_name = get_str(re_xml, "name")

            reportelem_qname = QName.from_string(
                f"{{{reportelem_url}}}{reportelem_name}", qname_nsmap
            )

            # check cache
            if reportelem_qname not in report_elements.keys():
                # TODO: update
                # create the report element
                factory_result = XMLReportElementFactory.create(
                    re_xml, reportelem_qname, []
                )
                if factory_result is None:
                    continue

                elem_id, reportelem = factory_result

                report_elements[reportelem_qname] = reportelem
                if elem_id is not None:
                    id_to_report_element[elem_id] = reportelem

                # if the report element is a dimension, then check if there is a typedDomainRef
                if isinstance(reportelem, Dimension):
                    # get the prefix binding for the xbrldt namespace in the context of the schema
                    # Note: I cannot get this via QName.get_nsmap() because there might be multiple schemas with different prefix bindings for the xbrldt namespace
                    xbrldt_prefix = etree.getroot().nsmap["xbrldt"]
                    typed_domain_ref = f"{{{xbrldt_prefix}}}typedDomainRef"

                    # check if the xml element has a xbrldt:typedDomainRef attributeq
                    if typed_domain_ref in re_xml.attrib:
                        # get the prefix binding for the xbrldt namespace in the context of the schema

                        # ref_full = re_xml.get(typed_domain_ref)
                        ref_full = get_str(re_xml, typed_domain_ref)

                        # get the schema and the element id
                        ref_schema_name, ref_id = ref_full.split("#")

                        # get the right schema
                        if ref_schema_name == "":
                            refschema = etree
                        else:
                            refschema = file_manager.get_file(ref_schema_name)

                        # get the element the ref is pointing to
                        # it is an xs:element with the id attr being the ref
                        ref_xml = refschema.find(
                            f".//*[@id='{ref_id}']", namespaces=None
                        )
                        if ref_xml is None:
                            raise ValueError(
                                f"the schema {refschema} does not contain an element with the id {ref_id}"
                            )

                        # get the type of ref_xml
                        # ref_type = ref_xml.get("type")
                        ref_type = get_str(ref_xml, "type")

                        # convert to QName
                        ref_type_qname = QName.from_string(
                            ref_type, qname_nsmap
                        )

                        # set the type of the dimension
                        # TODO: ref_type is a str. It should be a QName or type
                        reportelem.make_typed(ref_type_qname)

    return report_elements, id_to_report_element
