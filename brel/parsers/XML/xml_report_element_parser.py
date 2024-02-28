"""
This module contains the function to parse the report elements from the xbrl instance.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.5
- date: 05 February 2024

====================
"""

import lxml.etree

from brel import QName, QNameNSMap
from brel.parsers.utils import get_str
from brel.reportelements import Dimension, IReportElement

from ..dts import IFileManager
from .xml_report_element_factory import XMLReportElementFactory


def parse_report_elements_xml(
    file_manager: IFileManager,
    etrees: list[lxml.etree._ElementTree],
    qname_nsmap: QNameNSMap,
) -> tuple[dict[QName, IReportElement], dict[str, IReportElement], list[Exception]]:
    """
    Parse the concepts.
    :param file_manager: The file manager that contains the xbrl instance and the schemas.
    :param qname_nsmap: The QNameNSMap that contains all the namespaces used in the filing.
    :returns:
    - A dictionary mapping the QName to the report element. Contains all the report elements in the filing, even those that are not reported against.
    - A dictionary mapping the id of the xml element to the report element. This is useful for resolving hrefs.
    - A list of exceptions that occurred during parsing.
    """

    report_elements: dict[QName, IReportElement] = {}
    id_to_report_element: dict[str, IReportElement] = {}
    errors: list[Exception] = []

    for etree in etrees:
        try:
            reportelem_url = get_str(etree.getroot(), "targetNamespace")
        except Exception as e:
            errors.append(e)
            continue

        # get all the concept xml elements in the schema that have an attribute name
        re_xmls = etree.findall(".//{*}element[@name]", namespaces=None)
        for re_xml in re_xmls:
            try:
                reportelem_name = get_str(re_xml, "name")
            except Exception as e:
                errors.append(e)
                continue

            try:
                reportelem_qname = QName.from_string(f"{{{reportelem_url}}}{reportelem_name}", qname_nsmap)
            except Exception as e:
                errors.append(e)
                continue

            # check cache
            if reportelem_qname not in report_elements.keys():
                # create the report element
                factory_result = XMLReportElementFactory.create(re_xml, reportelem_qname, [])
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
                        try:
                            ref_full = get_str(re_xml, typed_domain_ref)
                        except Exception as e:
                            errors.append(e)
                            continue

                        # get the schema and the element id
                        ref_schema_name, ref_id = ref_full.split("#")

                        # get the right schema
                        try:
                            if ref_schema_name == "":
                                refschema = etree
                            else:
                                refschema = file_manager.get_file(ref_schema_name)
                        except Exception as e:
                            errors.append(e)
                            continue

                        # get the element the ref is pointing to
                        # it is an xs:element with the id attr being the ref
                        ref_xml = refschema.find(f".//*[@id='{ref_id}']", namespaces=None)
                        if ref_xml is None:
                            errors.append(
                                ValueError(f"the schema {refschema} does not contain an element with the id {ref_id}")
                            )
                            continue

                        # get the type of ref_xml
                        try:
                            ref_type = get_str(ref_xml, "type")
                        except Exception as e:
                            errors.append(e)
                            continue

                        # convert to QName
                        try:
                            ref_type_qname = QName.from_string(ref_type, qname_nsmap)
                        except Exception as e:
                            errors.append(e)
                            continue

                        # set the type of the dimension
                        reportelem.make_typed(ref_type_qname)

    return report_elements, id_to_report_element, errors
