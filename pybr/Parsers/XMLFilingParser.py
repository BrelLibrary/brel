import os
import requests
import lxml
import lxml.etree
from typing import Iterable
from io import BytesIO
from pybr.Parsers.IFilingParser import IFilingParser
from pybr import PyBRContext, PyBRConcept, PyBRUnit, PyBRAspect, PyBRFact, QName
import editdistance

class XMLFilingParser(IFilingParser):
    def __init__(self, filing_path: str, encoding="UTF-8") -> None:
        super().__init__()
        self.__filing_type = "XML"
        self.__encoding = encoding
        self.__parser = lxml.etree.XMLParser(encoding=self.__encoding)
        self.__cache_location = "pybr/dts_cache/"
        self.__filing_location = filing_path
        self.__print_prefix = f"{'[XMLFilingParser]':<20}"

        self.__concept_cache = {}
        self.__unit_cache = {}

        schema_filename = None
        instance_filename = None

        # find the filenames of the schema and the instance
        all_filenames = os.listdir(self.__filing_location)
        for filename in all_filenames:
            if filename.endswith(".xsd"):
                schema_filename = filename
            elif filename.endswith("_htm.xml"):
                instance_filename = filename
        
        # if the filenames are not found, raise an error
        if schema_filename is None:
            raise ValueError("No schema file found")
        if instance_filename is None:
            raise ValueError("No instance file found")
        
        # load the instance
        self.xbrl_instance = lxml.etree.parse(self.__filing_location + instance_filename, self.__parser)
        self.xbrl_schema_cache = {}

        # load the schema and all its dependencies
        self.print("Resolving DTS...")
        self.__load_schema(schema_filename)
        self.print("DTS resolved!")
    
    def print(self, output: str):
        """
        Print a message with the prefix [XMLFilingParser].
        """
        print(self.__print_prefix, output)

    def __load_schema(self, xsd_url, referencing_schema_url="."):

        # file_name = filename_from_url(xsd_url)
        file_name = xsd_url.split("/")[-1]

        is_url_remote = xsd_url.startswith("http")
        is_in_filing = file_name in os.listdir(self.__filing_location)
        is_cached = file_name in os.listdir(self.__cache_location)

        if is_cached:
            # if the file is cached, load it from the cache
            # with open(self.__cache_location + file_name, "rb") as f:
            #     xsd_content = f.read()
            # self.print(f"> Schema {xsd_url} and dependencies already in cache")
            pass

        elif is_url_remote:
            # if the file is online, load it from the url
            response = requests.get(xsd_url)
            xsd_content = response.content

        elif is_in_filing:
            # otherwise load it from the current directory
            with open(self.__filing_location + xsd_url, "rb") as f:
                xsd_content = f.read()

        else:
            # if the file is not cached, online or in the filing, then it must be in the file system of the
            # schema that is referencing it
            # so I transform the xsd_url from a local file path to a url

            xsd_url = referencing_schema_url.rsplit("/", 1)[0] + "/" + xsd_url

            response = requests.get(xsd_url)
            xsd_content = response.content
        
        if not is_cached:
            parser = self.__parser
            xsd_tree = lxml.etree.parse(BytesIO(xsd_content), parser=parser)

            # check all the imports in the schema
            imports = xsd_tree.findall("{http://www.w3.org/2001/XMLSchema}import")
            for xsd_import in imports:
                # for all imports, load the schema recursively
                # and add it to the current schema
                schema_location = xsd_import.attrib["schemaLocation"]
                self.__load_schema(schema_location, xsd_url)
            
            # write the schema to the cache with the updated imports
            with open(self.__cache_location + file_name, "wb") as f:
                f.write(lxml.etree.tostring(xsd_tree))
            print(f"Loaded schema {xsd_url} into cache")

    
    def __get_concept_filename(self, qname: QName) -> str:
        """
        Checks all the files in the cache and returns the filename of the file that is closest to the qname.
        Filename is not the full path, just the name of the file.
        @param qname: The QName of the concept.
        @return: The filename of the file that is closest to the qname as a string.
        """
        # print current working directory

        # first get all the files in the cache
        filenames = os.listdir(self.__cache_location)

        # strip part of the domain
        domain = qname.get_URL().split(".")[-1]

        # find the closest file name using edit distance
        closest_distance = 1000
        closest_filename = ""
        for filename in filenames:
            distance = editdistance.eval(filename, domain)
            if distance < closest_distance:
                closest_distance = distance
                closest_filename = filename
        
        return closest_filename

    
    def parse(self) -> dict:
        """
        Parse the filing.
        @return: the different components of the filing as a dictionary.
        Currently returns the following:
        - filing_type: str. The type of the filing. Currently "XML".
        - facts: list[PyBRFact]. The facts in the filing.
        - concepts: list[PyBRConcept]. The concepts in the filing, even those that are not reported.
        """
        result = {
            "filing_type": self.get_filing_type(),
            "facts": self.parse_facts(),
            "concepts": self.parse_concepts()
        }

        return result

    def parse_facts(self) -> list[PyBRFact]:
        """
        Parse the facts.
        """
        # get all xml elements in the instance that have a contextRef attribute
        xml_facts = self.xbrl_instance.findall(".//*[@contextRef]", namespaces=None)

        url_to_prefix = {v: k for k, v in xml_facts[0].nsmap.items()}

        facts = []
        for xml_fact in xml_facts:

            # then get the context id and search for the context xml element
            context_id = xml_fact.attrib["contextRef"]
            
            # the context xml element has the tag {{*}}context and the id is the context_id
            xml_context = self.xbrl_instance.find(f"{{*}}context[@id='{context_id}']")

            # then parse the context
            context = PyBRContext.from_xml(xml_context)
 
            # get the unit id
            unit_id = xml_fact.get("unitRef")

            # if there is a unit id, then find the unit xml element, parse it and add it to the context
            if unit_id:
                # check cache
                if unit_id in self.__unit_cache:
                    unit = self.__unit_cache[unit_id]
                else:
                    xml_unit = self.xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']")
                    unit = PyBRUnit.from_xml(xml_unit)
                    self.__unit_cache[unit_id] = unit
                
                context.add_aspect_value(PyBRAspect.UNIT, unit)

            # get the concept name              
            concept_name = xml_fact.tag                
            concept_localname = concept_name.split("}")[-1]
            concept_url = concept_name.split("}")[0][1:]
            concept_prefix = url_to_prefix[concept_url]
            concept_qname = QName(concept_url, concept_prefix, concept_localname)

            # check concept cache
            if concept_qname in self.__concept_cache:
                concept = self.__concept_cache[concept_qname]
            else:
                # get the concept xml element
                concept_filename = self.__get_concept_filename(concept_qname)

                # check schema cache
                if concept_filename in self.xbrl_schema_cache:
                    concepts_xml = self.xbrl_schema_cache[concept_filename]
                else:
                    concepts_xml = lxml.etree.parse(self.__cache_location + concept_filename, self.__parser)
                    self.xbrl_schema_cache[concept_filename] = concepts_xml
                concept_xml = concepts_xml.find(f"{{*}}element[@name='{concept_localname}']")

                # parse the concept
                concept = PyBRConcept.from_xml(concept_xml, concept_qname)
                self.__concept_cache[concept_qname] = concept

            # add the concept to the context
            context.add_aspect_value(PyBRAspect.CONCEPT, concept)

            # create the fact
            fact = PyBRFact.from_xml(xml_fact, context)

            facts.append(fact)
        
        return facts
    
    def parse_concepts(self) -> list[PyBRConcept]:
        """
        Parse the concepts.
        @return: A list of all the concepts in the filing, even those that are not reported.
        """
        concepts = []

        # get all files in the cache
        filenames = os.listdir(self.__cache_location)

        for filename in filenames:
            if not filename.endswith(".xsd"):
                continue

            # check schema cache
            if filename in self.xbrl_schema_cache:
                schema_xml = self.xbrl_schema_cache[filename]
            else:
                schema_xml = lxml.etree.parse(self.__cache_location + filename, self.__parser)
                self.xbrl_schema_cache[filename] = schema_xml
            
            concept_url = schema_xml.getroot().attrib["targetNamespace"]
            concept_prefix = ""
            for prefix, url in schema_xml.getroot().nsmap.items():
                if url == concept_url:
                    concept_prefix = prefix
                    break
            
            # get all the concept xml elements in the schema that have an attribute name
            concept_xmls = schema_xml.findall(".//{*}element[@name]", namespaces=None)
            for concept_xml in concept_xmls:
                concept_name = concept_xml.attrib["name"]
                concept_qname = QName(concept_url, concept_prefix, concept_name)

                # check cache
                if concept_qname in self.__concept_cache:
                    concept = self.__concept_cache[concept_qname]
                else:
                    concept = PyBRConcept.from_xml(concept_xml, concept_qname)
                    self.__concept_cache[concept_qname] = concept

                concepts.append(concept)
        
        return concepts
    
    def get_filing_type(self) -> str:
        """
        Get the filing type. Returns "XML".
        """
        return "XML"
    
        
