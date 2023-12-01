import os
import lxml
import lxml.etree

# import BytesIO
from io import BytesIO

from pybr.reportelements import IReportElement, PyBRDimension, PyBRConcept
from pybr.characteristics import PyBRConceptCharacteristic, PyBRUnitCharacteristic
from pybr import QName, BrelLabel, PyBRContext, PyBRFact, PyBRComponent
from pybr.parsers import IFilingParser
from pybr.parsers.dts import XMLSchemaManager, ISchemaManager
from pybr.networks import INetwork
from pybr.parsers.utils.lxml_utils import get_all_nsmaps
from pybr.parsers.XML.xml_namespace_normalizer import normalize_nsmap
from collections import defaultdict

from .XML.xml_labels_parser import parse_labels_xml
from .XML.xml_component_parser import parse_components_xml
from .XML.xml_report_element_parser import parse_report_elements_xml
from .XML.xml_facts_parser import parse_facts_xml
from .XML.networks.xml_network_parser import networks_from_xmls

import validators

import requests


from typing import cast

class XMLFilingParser(IFilingParser):
    def __init__(self, filing_path: str, encoding="UTF-8") -> None:
        super().__init__()

        class SchemaResolver(lxml.etree.Resolver):
            def __init__(this, schema_manager: XMLSchemaManager) -> None:
                this.__schema_manager = schema_manager
            
            def resolve(this, system_url: str = "", public_id: str = "", context=None):
                print (f"Resolving {system_url}")
                # if system_url.endswith(".xsd"):
                #     filepath = this.__schema_manager.cache_location + this.__schema_manager.url_to_filename(system_url)
                #     print(f"Filepath: {filepath}")
                #     print(f"system_url: {system_url}")
                #     return this.resolve_file(open(filepath, "rb"), context, base_url=system_url)
                # else:
                #     return super().resolve(system_url, public_id, context)
                
                # use requests to get the schema
                if system_url.startswith("http"):
                    response = requests.get(system_url)
                    print(response.status_code)
                    try:
                        result = super().resolve_string(response.text, context, base_url=system_url)
                        print(result)
                        return result
                    except Exception as e:
                        print(e)
                        raise e

                else:
                    print("fallback to default resolver")
                    return super().resolve(system_url, public_id, context)



        self.__filing_type = "XML"
        self.__encoding = encoding
        self.__parser = lxml.etree.XMLParser(encoding=self.__encoding)
        self.__filing_location = filing_path
        self.__print_prefix = f"{'[XMLFilingParser]':<20}"

        instance_filename = None
        labels_filename = None
        presentation_filename = None
        calculation_filename = None
        definition_filename = None
        schema_filename = None

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
            elif filename.endswith(".xsd"):
                schema_filename = filename
        
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
        
        
        # load the schema and all its dependencies
        self.__print("Resolving DTS...")
        self.__schema_manager = XMLSchemaManager("pybr/dts_cache/", filing_path, self.__parser)
        self.__print("DTS resolved!")

        self.__parser.resolvers.add(SchemaResolver(self.__schema_manager))

        # load the instance
        self.__print("Loading instance...")
        self.xbrl_instance = lxml.etree.parse(self.__filing_location + instance_filename, self.__parser)
        self.__print("Instance loaded!")


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

        # self.__print("validating instance...")
        # validator = lxml.etree.XMLSchema(self.__schema_manager.get_schema(schema_filename))
        # print(validator.validate(self.xbrl_instance))
        # self.__print("instance validated!")


        
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

        nsmap, redirects = normalize_nsmap(nsmaps)

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
    
    def parse_report_elements(self, labels: dict[QName, list[BrelLabel]]) -> dict[QName, IReportElement]:
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
    

    def parse_labels(self) -> dict[QName, list[BrelLabel]]:
        """
        Parse the labels
        @return: A list of all the labels in the filing
        """
        return parse_labels_xml(self.xbrl_labels)
    
    def parse_networks(self, report_elements: dict[QName, IReportElement]) -> dict[str, list[INetwork]]:
        """
        Parse the networks.
        @param report_elements: A dictionary containing ALL report elements that the networks report against.
        @return: A dictionary of all the networks in the filing.
        """
        return networks_from_xmls(
            [
                self.xbrl_presentation_graph,
                self.xbrl_calculation_graph,
                self.xbrl_definition_graph,
                self.xbrl_labels
            ] + self.__schema_manager.get_all_schemas(),
            report_elements
        )

    def parse_components(
            self, 
            report_elements: dict[QName, IReportElement], 
            networks: dict[str, list[INetwork]]
            ) -> tuple[list[PyBRComponent], dict[QName, IReportElement]]:
        """
        Parse the components.
        @param report_elements: A dictionary containing ALL report elements that the components report against.
        @param networks: A dictionary containing ALL networks that the components report against. 
        The keys are the component names, the values are lists of networks for that component.
        @return: 
         - A list of all the components in the filing.
         - A dictionary of all the report elements in the filing. These might have been altered by the components.
        """
        return parse_components_xml(
            self.__schema_manager.get_all_schemas(),
            networks,
            report_elements
        )
        
    def get_filing_type(self) -> str:
        """
        Get the filing type. Returns "XML".
        """
        return self.__filing_type
    
        
