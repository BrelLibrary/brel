import os
import lxml
import lxml.etree

from pybr.reportelements import IReportElement, PyBRDimension, PyBRConcept
from pybr.characteristics import PyBRConceptCharacteristic, PyBRUnitCharacteristic
from pybr import QName, PyBRLabel, PyBRContext, PyBRFact, PyBRComponent
from pybr.parsers import IFilingParser
from pybr.parsers.dts import XMLSchemaManager
from pybr.networks import PresentationNetwork, CalculationNetwork
from pybr.parsers.utils.lxml_utils import get_all_nsmaps, combine_nsmaps
from collections import defaultdict

from .XML.xml_labels_parser import parse_labels_xml
from .XML.xml_component_parser import parse_components_xml
from .XML.xml_report_element_parser import parse_report_elements_xml
from .XML.xml_facts_parser import parse_facts_xml


from typing import cast

class XMLFilingParser(IFilingParser):
    def __init__(self, filing_path: str, encoding="UTF-8") -> None:
        super().__init__()
        self.__filing_type = "XML"
        self.__encoding = encoding
        self.__parser = lxml.etree.XMLParser(encoding=self.__encoding)
        self.__cache_location = "pybr/dts_cache/"
        self.__filing_location = filing_path
        self.__print_prefix = f"{'[XMLFilingParser]':<20}"

        instance_filename = None
        labels_filename = None
        presentation_filename = None
        calculation_filename = None
        definition_filename = None

        # find the filenames of the schema and the instance
        all_filenames = os.listdir(self.__filing_location)
        for filename in all_filenames:
            if filename.endswith("_htm.xml"):
                instance_filename = filename
            elif filename.endswith("_lab.xml"):
                labels_filename = filename
            elif filename.endswith("_pre.xml"):
                presentation_filename = filename
            elif filename.endswith("_cal.xml"):
                calculation_filename = filename
            elif filename.endswith("_def.xml"):
                definition_filename = filename
        
        # if the filenames are not found, raise an error
        if instance_filename is None:
            raise ValueError("No instance file found")
        if labels_filename is None:
            raise ValueError("No labels file found")
        if presentation_filename is None:
            raise ValueError("No presentation file found")
        if calculation_filename is None:
            raise ValueError("No calculation file found")
        if definition_filename is None:
            raise ValueError("No definition file found")
        
        # load the instance
        self.__print("Loading instance...")
        self.xbrl_instance = lxml.etree.parse(self.__filing_location + instance_filename, self.__parser)
        self.__print("Instance loaded!")

        # load the schema and all its dependencies
        self.__print("Resolving DTS...")
        self.__schema_manager = XMLSchemaManager("pybr/dts_cache/", filing_path)
        self.__print("DTS resolved!")

        # load the labels
        self.__print("Loading labels...")
        self.xbrl_labels = lxml.etree.parse(self.__filing_location + labels_filename, self.__parser)
        self.__print("Labels loaded!")

        # load the presentation graph
        self.__print("Loading presentation graph...")
        self.xbrl_presentation_graph = lxml.etree.parse(self.__filing_location + presentation_filename, self.__parser)
        self.__print("Presentation graph loaded!")

        # load the calculation graph
        self.__print("Loading calculation graph...")
        self.xbrl_calculation_graph = lxml.etree.parse(self.__filing_location + calculation_filename, self.__parser)
        self.__print("Calculation graph loaded!")

        # load the definition graph
        self.__print("Loading definition graph...")
        self.xbrl_definition_graph = lxml.etree.parse(self.__filing_location + definition_filename, self.__parser)
        self.__print("Definition graph loaded!")
        
        # normalize and bootstrap the QName nsmap
        self.__print("Normalizing nsmap...")
        self.__bootstrap_qname_nsmap()
        self.__print("Nsmap normalized!")

        self.__print("XMLFilingParser initialized!")
        print("-"*50)
    
    def __bootstrap_qname_nsmap(self):
        if self.xbrl_instance is None:
            raise ValueError("Instance not loaded")
        
        instance_xml_trees = [
            self.xbrl_instance,
            self.xbrl_labels,
            self.xbrl_presentation_graph,
            self.xbrl_calculation_graph,
            self.xbrl_definition_graph
        ]

        schema_xml_trees = self.__schema_manager.get_all_schemas()

        nsmaps = get_all_nsmaps(instance_xml_trees)
        nsmaps.extend(get_all_nsmaps(schema_xml_trees))
        # add xml namespace to a random nsmap
        nsmaps[0]["xml"] = "http://www.w3.org/XML/1998/namespace"

        nsmap, redirects = combine_nsmaps(nsmaps)

        print("[QName] Prefix mappings:")
        for prefix, url in nsmap.items():
            QName.add_to_nsmap(url, prefix)
            print(f"> {prefix:20} -> {url}")

        print("[QName] Prefix redirects:")
        for redirect_from, redirect_to in redirects.items():
            QName.set_redirect(redirect_from, redirect_to)
            print(f"> {redirect_from:10} -> {redirect_to}")
        print("Note: Prefix redirects are not recommended.")

    
    def __print(self, output: str):
        """
        Print a message with the prefix [XMLFilingParser].
        """
        print(self.__print_prefix, output)
    
    def parse_report_elements(self, labels: dict[QName, list[PyBRLabel]]) -> dict[QName, IReportElement]:
        """
        Parse the concepts.
        @return: A list of all the concepts in the filing, even those that are not reported.
        """
        return parse_report_elements_xml(
            self.__schema_manager,
            labels
        )
    

    def parse_facts(self, report_elements: dict[QName, IReportElement]) -> list[PyBRFact]:
        """
        Parse the facts.
        """
        return parse_facts_xml(
            self.xbrl_instance,
            report_elements
        )
    

    def parse_labels(self) -> dict[QName, list[PyBRLabel]]:
        """
        Parse the labels
        @return: A list of all the labels in the filing
        """
        return parse_labels_xml(self.xbrl_labels)
    

    def parse_components(self, report_elements: dict[QName, IReportElement]) -> tuple[list[PyBRComponent], dict[QName, IReportElement]]:
        """
        Parse the components.
        @return: 
         - A list of all the components in the filing.
         - A dictionary of all the report elements in the filing. These might have been altered by the components.
        """
        return parse_components_xml(
            self.__schema_manager.get_all_schemas(),
            [self.xbrl_presentation_graph, self.xbrl_calculation_graph, self.xbrl_definition_graph],
            report_elements
        )
        
    def get_filing_type(self) -> str:
        """
        Get the filing type. Returns "XML".
        """
        return self.__filing_type
    
        
