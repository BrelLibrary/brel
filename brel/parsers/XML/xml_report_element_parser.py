"""
This module contains the function to parse the report elements from the xbrl instance.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 16 April 2025

====================
"""

import lxml.etree

from brel import QName, QNameNSMap
from brel.parsers.utils import get_str_attribute
from brel.parsers.utils.error_utils import error_on_none
from brel.reportelements import Dimension

from brel.parsers.dts.i_file_manager import IFileManager
from .xml_report_element_factory import XMLReportElementFactory
from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.contexts.filing_context import FilingContext


def parse_report_elements_xml(
    context: FilingContext,
    file_manager: IFileManager,
    etrees: list[lxml.etree._ElementTree],  # type: ignore
) -> None:
    """
    Parse the concepts.
    :param file_manager: The file manager that contains the xbrl instance and the schemas.
    :param qname_nsmap: The QNameNSMap that contains all the namespaces used in the filing.
    :returns:
    - A dictionary mapping the QName to the report element. Contains all the report elements in the filing, even those that are not reported against.
    - A dictionary mapping the id of the xml element to the report element. This is useful for resolving hrefs.
    - A list of exceptions that occurred during parsing.
    """

    error_repository = context.get_error_repository()
    report_element_repository = context.get_report_element_repository()
    qname_nsmap = context.get_nsmap()

    for etree in etrees:
        re_xmls = error_repository.upsert_on_error(
            lambda: etree.findall(".//{*}schemaLocation", namespaces=None)
        )

        target_namespace_url = get_str_attribute(etree.getroot(), "targetNamespace")

        re_xmls = etree.findall(".//{*}element[@name]", namespaces=None)
        for re_xml in re_xmls:
            error_repository.upsert_on_error(
                lambda: parse_report_element(
                    report_element_repository=report_element_repository,
                    file_manager=file_manager,
                    qname_nsmap=qname_nsmap,
                    report_element_xml=re_xml,
                    target_namespace_url=target_namespace_url,
                )
            )


def parse_report_element(
    report_element_repository: ReportElementRepository,
    file_manager: IFileManager,
    qname_nsmap: QNameNSMap,
    report_element_xml: lxml.etree._Element,  # type: ignore
    target_namespace_url: str,
):
    qname_tag = get_str_attribute(report_element_xml, "name")
    qname = QName.from_string(f"{{{target_namespace_url}}}{qname_tag}", qname_nsmap)
    report_element = XMLReportElementFactory.create(report_element_xml, qname, [])
    if report_element and not report_element_repository.has_qname(qname):
        report_element_repository.upsert(report_element)

        # TODO schmidi fix this. looks hacky
        if isinstance(report_element, Dimension):
            xbrldt_prefix = report_element_xml.nsmap["xbrldt"]
            typed_domain_ref = f"{{{xbrldt_prefix}}}typedDomainRef"

            if typed_domain_ref in report_element_xml.attrib:
                ref_full = get_str_attribute(report_element_xml, typed_domain_ref)
                ref_schema_name, ref_id = ref_full.split("#")

                refschema = (
                    file_manager.get_file(ref_schema_name)
                    if ref_schema_name
                    else report_element_xml
                )
                ref_xml = error_on_none(
                    refschema.find(f".//*[@id='{ref_id}']", namespaces=None),
                    f"Could not find reference {ref_id} in {ref_schema_name}",
                )

                ref_type = get_str_attribute(ref_xml, "type")
                ref_type_qname = QName.from_string(ref_type, qname_nsmap)

                report_element.make_typed(ref_type_qname)
