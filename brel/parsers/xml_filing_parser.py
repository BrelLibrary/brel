import os
import lxml
import lxml.etree

from brel.reportelements import IReportElement
from brel import QName, Fact, Component, QNameNSMap
from brel.parsers import IFilingParser
from brel.parsers.dts import XMLSchemaManager
from brel.networks import INetwork
from brel.parsers.utils.lxml_utils import get_all_nsmaps
from brel.parsers.XML.xml_namespace_normalizer import normalize_nsmap

from .XML.xml_component_parser import parse_components_xml
from .XML.xml_report_element_parser import parse_report_elements_xml
from .XML.xml_facts_parser import parse_facts_xml
from .XML.networks.xml_networks_parser import networks_from_xmls

DEBUG = False

class XMLFilingParser(IFilingParser):
    def __init__(
            self, 
            instance_filepaths: str,
            networks_filepaths: list[str] | None = None,
            encoding: str = "utf-8",
            ) -> None:
        
        if networks_filepaths is None:
            networks_filepaths = []

        self.__filing_type = "XML"
        self.__encoding = encoding
        self.__parser = lxml.etree.XMLParser(encoding=self.__encoding)
        self.__filing_location = instance_filepaths.rsplit("/", 1)[0] + "/"
        self.__print_prefix = f"{'[XMLFilingParser]':<20}"
        
        # load the instance
        if DEBUG:  # pragma: no cover
            self.__print("Loading instance...")
        self.xbrl_instance = lxml.etree.parse(instance_filepaths, self.__parser)

        schemaref_elem = self.xbrl_instance.find(".//{*}schemaRef")
        if schemaref_elem is None:
            raise ValueError("No schemaRef element found in instance")
        else:
            # get the xlink:href attribute. I do it in this convoluted way because the namespace map is not generated yet
            href_attr = next(filter(lambda x: "href" in x, schemaref_elem.attrib.keys()), None)
            if href_attr is None:
                raise ValueError("No href attribute found in schemaRef element")

            schema_filename = schemaref_elem.get(href_attr)
        
        # load the schema and all its dependencies
        if DEBUG:  # pragma: no cover
            self.__print("Resolving DTS...")
        self.__schema_manager = XMLSchemaManager("brel/dts_cache/", self.__filing_location, schema_filename, self.__parser)

        if DEBUG:  # pragma: no cover
            self.__print("Loading Networks...")
        self.__xbrl_networks = []
        for network_filename in networks_filepaths:
            # load the network
            network = lxml.etree.parse(network_filename, self.__parser)
            self.__xbrl_networks.append(network)
        
        # normalize and bootstrap the QName nsmap
        if DEBUG:  # pragma: no cover
            self.__print("Normalizing nsmap...")
        self.__nsmap = self.__create_nsmap()

        if DEBUG:  # pragma: no cover
            self.__print("XMLFilingParser initialized!")
            print("-"*50)
    
    def __create_nsmap(self) -> QNameNSMap:
        if self.xbrl_instance is None:
            raise ValueError("Instance not loaded")
        
        instance_xml_trees = [
            self.xbrl_instance,
        ] + self.__xbrl_networks

        schema_xml_trees = self.__schema_manager.get_all_schemas()

        nsmaps = get_all_nsmaps(instance_xml_trees)
        nsmaps.extend(get_all_nsmaps(schema_xml_trees))
        # add xml namespace to a random nsmap
        nsmaps[0]["xml"] = "http://www.w3.org/XML/1998/namespace"

        normalizer_result = normalize_nsmap(nsmaps)
        nsmap = normalizer_result["nsmap"]
        redirects = normalizer_result["redirects"]
        renames = normalizer_result["renames"]

        qname_nsmap = QNameNSMap()

        if DEBUG:  # pragma: no cover
            print("[QName] Prefix mappings:")
        for prefix, url in nsmap.items():
            # QName.add_to_nsmap(url, prefix)
            qname_nsmap.add_to_nsmap(url, prefix)
            if DEBUG:  # pragma: no cover
                print(f"> {prefix:20} -> {url}")
        
        if DEBUG:  # pragma: no cover
            print("[QName] Prefix redirects:")
        for redirect_from, redirect_to in redirects.items():
            # QName.set_redirect(redirect_from, redirect_to)
            qname_nsmap.add_redirect(redirect_from, redirect_to)
            if DEBUG:  # pragma: no cover
                print(f"> {redirect_from:10} -> {redirect_to}")
        
        if DEBUG:  # pragma: no cover
            print("[QName] Prefix renames:")
        for rename_to, rename_from in renames.items():
            # QName.set_rename(rename_from, rename_to)
            qname_nsmap.add_rename(rename_from, rename_to)
            if DEBUG:
                print(f"> {rename_from:10} -> {rename_to}")
        
        if DEBUG:  # pragma: no cover
            print("Note: Prefix redirects are not recommended.")
        
        return qname_nsmap

    
    def __print(self, output: str):
        """
        Print a message with the prefix [XMLFilingParser].
        """
        if DEBUG:  # pragma: no cover
            print(self.__print_prefix, output)
    
    def parse_report_elements(self) -> dict[QName, IReportElement]:
        """
        Parse the concepts.
        @return: A list of all the concepts in the filing, even those that are not reported.
        """
        return parse_report_elements_xml(self.__schema_manager, self.__nsmap)
    

    def parse_facts(self, report_elements: dict[QName, IReportElement]) -> list[Fact]:
        """
        Parse the facts.
        """
        return parse_facts_xml(
            self.xbrl_instance,
            report_elements,
            self.__nsmap
        )
    
    def parse_networks(self, report_elements: dict[QName, IReportElement]) -> dict[str, list[INetwork]]:
        """
        Parse the networks.
        @param report_elements: A dictionary containing ALL report elements that the networks report against.
        @return: A dictionary of all the networks in the filing.
        """
        return networks_from_xmls(
            self.__xbrl_networks + self.__schema_manager.get_all_schemas(),
            self.__nsmap,
            report_elements
        )

    def parse_components(
            self, 
            report_elements: dict[QName, IReportElement], 
            networks: dict[str, list[INetwork]]
            ) -> tuple[list[Component], dict[QName, IReportElement]]:
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
            report_elements,
            self.__nsmap
        )
        
    def get_filing_type(self) -> str:
        """
        Get the filing type. Returns "XML".
        """
        return self.__filing_type
    
        
