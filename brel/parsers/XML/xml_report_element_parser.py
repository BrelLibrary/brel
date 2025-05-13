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

from brel.parsers.XML.xml_report_element_factory import XMLReportElementFactory
from brel.parsers.utils.error_utils import error_on_none
from brel.parsers.utils.lxml_utils import (
    find_elements,
    get_str_attribute,
    has_str_attribute,
)
from brel.qnames.qname_utils import (
    qname_from_str,
    to_clark_notation,
    to_namespace_localname_notation,
)
from brel.reportelements import Dimension
from brel.services.xml.xml_service import XMLService

from brel.data.report_element.report_element_repository import ReportElementRepository
from brel.contexts.filing_context import FilingContext


def parse_report_elements_xml(
    context: FilingContext,
) -> None:
    error_repository = context.get_error_repository()
    xml_service = context.get_xml_service()
    report_element_repository = context.get_report_element_repository()

    for etree in xml_service.get_all_etrees():
        if not has_str_attribute(etree.getroot(), "targetNamespace"):
            continue

        re_xmls = error_repository.upsert_on_error(
            lambda: find_elements(etree, ".//xsi:schemaLocation"),
        )

        target_namespace_url = get_str_attribute(etree.getroot(), "targetNamespace")

        re_xmls = find_elements(etree, ".//xs:element[@name]")
        for re_xml in re_xmls:
            error_repository.upsert_on_error(
                lambda: parse_report_element(
                    report_element_repository=report_element_repository,
                    xml_service=xml_service,
                    current_etree=etree,
                    report_element_xml=re_xml,
                    target_namespace_url=target_namespace_url,
                )
            )


def parse_report_element(
    report_element_repository: ReportElementRepository,
    xml_service: XMLService,
    current_etree: lxml.etree._ElementTree,  # type: ignore
    report_element_xml: lxml.etree._Element,  # type: ignore
    target_namespace_url: str,
):
    qname_tag = get_str_attribute(report_element_xml, "name")
    qname = qname_from_str(
        to_clark_notation(target_namespace_url, qname_tag), report_element_xml
    )
    report_element = XMLReportElementFactory.create(report_element_xml, qname, [])
    if report_element and not report_element_repository.has_qname(qname):
        report_element_repository.upsert(report_element)

        if isinstance(report_element, Dimension):
            typed_domain_ref = qname_from_str(
                to_namespace_localname_notation("xbrldt", "typedDomainRef"),
                report_element_xml,
            )

            if has_str_attribute(report_element_xml, typed_domain_ref):
                ref_full = get_str_attribute(report_element_xml, typed_domain_ref)
                ref_schema_name, ref_id = ref_full.split("#")
                refschema = (
                    xml_service.get_etree(ref_schema_name)
                    if ref_schema_name
                    else current_etree
                )
                ref_xml = error_on_none(
                    refschema.find(f".//*[@id='{ref_id}']", namespaces=None),
                    f"Could not find reference {ref_id} in {ref_schema_name}",
                )
                ref_type = get_str_attribute(ref_xml, "type")
                ref_type_qname = qname_from_str(ref_type, ref_xml)
                report_element.make_typed(ref_type_qname)
