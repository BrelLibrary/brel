import lxml
import lxml.etree

from ..dts import ISchemaManager
from pybr.reportelements import IReportElement, PyBRDimension
from pybr import QName, PyBRLabel

from .xml_report_element_factory import XMLReportElementFactory

def parse_report_elements_xml(
        schema_manager: ISchemaManager,
        labels: dict[QName, list[PyBRLabel]]) -> dict[QName, IReportElement]:
    """
    Parse the concepts.
    @return: A list of all the concepts in the filing, even those that are not reported.
    """

    report_elements: dict[QName, IReportElement] = {}
    
    for schema_xml in schema_manager.get_all_schemas():
        
        reportelem_url = schema_xml.getroot().attrib["targetNamespace"]
        reportelem_prefix = ""
        for prefix, url in schema_xml.getroot().nsmap.items():
            if url == reportelem_url:
                reportelem_prefix = prefix
                break
        
        # get all the concept xml elements in the schema that have an attribute name
        re_xmls = schema_xml.findall(".//{*}element[@name]", namespaces=None)
        for re_xml in re_xmls:
            reportelem_name = re_xml.attrib["name"]
            reportelem_qname = QName.from_string(f"{reportelem_prefix}:{reportelem_name}")

            # check cache
            if reportelem_qname not in report_elements.keys():
                # TODO: update
                re_labels = labels.get(reportelem_qname, [])
                reportelem = XMLReportElementFactory.create(re_xml, reportelem_qname, re_labels)

                if reportelem is not None:
                    report_elements[reportelem_qname] = reportelem

                # if the report element is a dimension, then check if there is a typedDomainRef
                if isinstance(reportelem, PyBRDimension):
                    # get the prefix binding for the xbrldt namespace in the context of the schema
                    # Note: I cannot get this via QName.get_nsmap() because there might be multiple schemas with different prefix bindings for the xbrldt namespace
                    xbrldt_prefix = schema_xml.getroot().nsmap["xbrldt"]
                    typed_domain_ref = f"{{{xbrldt_prefix}}}typedDomainRef"

                    # check if the xml element has a xbrldt:typedDomainRef attributeq
                    if typed_domain_ref in re_xml.attrib:
                        # get the prefix binding for the xbrldt namespace in the context of the schema

                        ref_full = re_xml.get(typed_domain_ref)

                        # get the schema and the element id
                        ref_schema_name, ref_id = ref_full.split("#")

                        # get the right schema
                        if ref_schema_name == "":
                            refschema = schema_xml
                        else:
                            refschema = schema_manager.get_schema(ref_schema_name)
                        
                        # get the element the ref is pointing to
                        # it is an xs:element with the id attr being the ref
                        ref_xml = refschema.find(f".//*[@id='{ref_id}']", namespaces=None)

                        # get the type of ref_xml
                        ref_type = ref_xml.get("type")

                        # convert to QName
                        ref_type_qname = QName.from_string(ref_type)

                        # set the type of the dimension
                        # TODO: ref_type is a str. It should be a QName or type
                        reportelem.make_typed(ref_type_qname)
    
    return report_elements