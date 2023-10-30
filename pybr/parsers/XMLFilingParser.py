import os
import requests
import lxml
import lxml.etree
from pybr.parsers.IFilingParser import IFilingParser
from pybr.parsers.dts import XMLSchemaManager
from pybr import PyBRContext, PyBRConceptCharacteristic, PyBRUnitCharacteristic, PyBRAspect, PyBRFact, QName, PyBRLabel, PyBRComponent
from pybr.networks import PresentationNetwork
from pybr.parsers.XMLReportElementFactory import XMLReportElementFactory
from pybr import IReportElement

class XMLFilingParser(IFilingParser):
    def __init__(self, filing_path: str, encoding="UTF-8") -> None:
        super().__init__()
        self.__filing_type = "XML"
        self.__encoding = encoding
        self.__parser = lxml.etree.XMLParser(encoding=self.__encoding)
        self.__report_element_factory = XMLReportElementFactory()
        self.__cache_location = "pybr/dts_cache/"
        self.__filing_location = filing_path
        self.__print_prefix = f"{'[XMLFilingParser]':<20}"
        self.__report_elements = {}
        self.__unit_c_cache = {}
        self.__concept_c_cache = {}

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
        
        # TODO: Afaik not all of these files are required. e.g. the presentation graph is not required. So make this more permissive.
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

        # bootstrap the QName nsmap using the instance
        self.__print("Bootstrapping QName nsmap...")
        self.__bootstrap_qname_nsmap()
        self.__print("QName nsmap bootstrapped!")

        self.__print("XMLFilingParser initialized!")
        print("-"*50)
    
    def __bootstrap_qname_nsmap(self):
        if self.xbrl_instance is None:
            raise ValueError("Instance not loaded")
        
        # get the root element of the instance
        root = self.xbrl_instance.getroot()

        # get the namespace map of the root element
        nsmap = root.nsmap

        for prefix, url in nsmap.items():
            QName.add_to_nsmap(url, prefix)
        
        # also add the xml namespace
        # TODO: find a nicer fix
        QName.add_to_nsmap("http://www.w3.org/XML/1998/namespace", "xml")

    
    def __print(self, output: str):
        """
        Print a message with the prefix [XMLFilingParser].
        """
        print(self.__print_prefix, output)

    
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
            "filing type": self.get_filing_type(),
            "report elements": self.parse_report_elements(),
            "facts": self.parse_facts(self.__report_elements),
            "labels": self.parse_labels(self.__report_elements),
            "components": self.parse_components()
        }

        return result
    
    def parse_report_elements(self) -> list[IReportElement]:
        """
        Parse the concepts.
        @return: A list of all the concepts in the filing, even those that are not reported.
        """
        # TODO: currently parses all report elements as concepts. This is not correct.
        # add support for abstract, lineitem, dimension, hypercube and member
        report_elems = []

        # get all files in the cache
        filenames = os.listdir(self.__cache_location)

        for filename in filenames:
            if not filename.endswith(".xsd"):
                continue

            # check schema cache
            schema_xml = self.__schema_manager.get_schema(filename)
            
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
                reportelem_qname = QName(reportelem_url, reportelem_prefix, reportelem_name)

                # check cache
                if reportelem_qname in self.__report_elements:
                    reportelem = self.__report_elements[reportelem_qname]
                else:
                    # reportelem = PyBRConcept.from_xml(re_xml, reportelem_qname)
                    # self.__report_elements[reportelem_qname] = reportelem
                    reportelem = self.__report_element_factory.create(re_xml, reportelem_qname)
                    self.__report_elements[reportelem_qname] = reportelem

                report_elems.append(reportelem)
        
        return report_elems
    

    def parse_facts(self, report_elements: dict[QName, IReportElement]) -> list[PyBRFact]:
        """
        Parse the facts.
        """
        # get all xml elements in the instance that have a contextRef attribute
        xml_facts = self.xbrl_instance.findall(".//*[@contextRef]", namespaces=None)

        nsmap = QName.get_nsmap()

        facts = []
        for xml_fact in xml_facts:

            # then get the context id and search for the context xml element
            context_id = xml_fact.attrib["contextRef"]
            
            # the context xml element has the tag {{*}}context and the id is the context_id
            xml_context = self.xbrl_instance.find(f"{{*}}context[@id='{context_id}']")

            # then parse the context
            # TODO: instead of passing all report elements, only pass the ones that are actually used in the context
            # this can potentially save a lot of time
            context = PyBRContext.from_xml(xml_context, self.__report_elements)
 
            # get the unit id
            unit_id = xml_fact.get("unitRef")

            # if there is a unit id, then find the unit xml element, parse it and add it to the context
            if unit_id:
                # check cache
                if unit_id in self.__unit_c_cache:
                    unit = self.__unit_c_cache[unit_id]
                else:
                    xml_unit = self.xbrl_instance.find(f"{{*}}unit[@id='{unit_id}']")
                    unit = PyBRUnitCharacteristic.from_xml(xml_unit)
                    self.__unit_c_cache[unit_id] = unit
                
                context.add_characteristic(PyBRAspect.UNIT, unit)

            # get the concept name              
            concept_name = xml_fact.tag                
            concept_qname = QName.from_string(concept_name)

            if concept_qname in self.__concept_c_cache:
                concept_characteristic = self.__concept_c_cache[concept_qname]
            else:
                # the concept has to be in the report elements cache. otherwise it does not exist
                if concept_qname not in self.__report_elements.keys():
                    raise ValueError(f"Concept {concept_qname} not found in report elements")
                
                # wrap the concept in a characteristic
                concept = self.__report_elements[concept_qname]
                concept_characteristic = PyBRConceptCharacteristic(concept)

            # add the concept to the context
            context.add_characteristic(PyBRAspect.CONCEPT, concept_characteristic)

            # create the fact
            fact = PyBRFact.from_xml(xml_fact, context)

            facts.append(fact)
        
        return facts
    

    def parse_labels(self, report_elements: dict[QName, IReportElement]) -> list[PyBRLabel]:
        """
        Parse the labels
        @return: A list of all the labels in the filing
        """

        labels = []

        nsmap = QName.get_nsmap()

        # get all label xml elements
        # labels are xml elements with the tag link:label
        labels_xml = self.xbrl_labels.findall(".//link:label", namespaces=nsmap)

        for label_xml in labels_xml:
            label = PyBRLabel.from_xml(label_xml)
            labels.append(label)

            # get the xlink:label attribute
            # this attribute contains the label id
            label_id = label_xml.get("{" + nsmap["xlink"] + "}label")

            # get the corresponding labelarc xml element
            # this element has the tag link:labelArc and the xlink:to attribute is the label id
            labelarc_xml = self.xbrl_labels.find(f".//link:labelArc[@xlink:to='{label_id}']", namespaces=nsmap)

            # get the locator id from the xlink:from attribute
            locator_id = labelarc_xml.get("{" + nsmap["xlink"] + "}from")

            # get the matching locator
            # the locator has the tag link:loc and the xlink:label attribute is the locator id
            locator_xml = self.xbrl_labels.find(f".//link:loc[@xlink:label='{locator_id}']", namespaces=nsmap)

            # the xlink:href attribute of the locator contains the report element name
            # split the href into an url and the filename
            _, report_element_name = locator_xml.get("{" + nsmap["xlink"] + "}href").split("#")

            # turn the report element name into a QName
            # TODO: improve the segment that alters the report_element_name into a valid qname
            # this is a temporary fix
            # replace the last "_" with ":"
            report_element_name = report_element_name.rsplit("_", 1)[0] + ":" + report_element_name.rsplit("_", 1)[1]

            report_element_qname = QName.from_string(report_element_name)

            # get the report element
            report_element = report_elements[report_element_qname]

            # add the label to the report element
            report_element.add_label(label)


        return labels

    def parse_components(self) -> list[PyBRComponent]:
        """
        Parse the components.
        @return: A list of all the components in the filing.
        """

        # TODO: for now the implementation assumes that only the roles. either do it calculation/definition as well or even for all roles in all schemas
        components = []

        nsmap = QName.get_nsmap()

        # get all rolerefs in the presentation graph
        presentation_rolerefs = self.xbrl_presentation_graph.findall(".//{*}roleRef", namespaces=None)
        for presentation_roleref in presentation_rolerefs:
            # get the href attribute
            # TODO: remove the url part
            href = presentation_roleref.get("{http://www.w3.org/1999/xlink}href")
            # split the href into an url and the filename
            url, component_name = href.split("#")
            
            # load the schema
            schema_xml = self.__schema_manager.get_schema(url)

            # find the component xml element
            component_xml = schema_xml.find(f".//link:roleType[@id='{component_name}']", namespaces=nsmap)

            # TODO: actually parse the labels, presentation, calculation and definition graphs
            # right now it's just a mock
            
            # parse the presentation_network
            # first, get the roleuRI attr of the roleref
            role_uri = presentation_roleref.get("roleURI")
            # then get the link:presentationLink element with the xlink:role attribute equal to the role_uri
            # this element is the presentation network
            presentation_link_xml = self.xbrl_presentation_graph.find(f".//link:presentationLink[@xlink:role='{role_uri}']", namespaces=nsmap)
            # TODO: make report elements an arg of parse_components instead of getting it via self.__report_elements
            presentation_network = PresentationNetwork.from_xml(presentation_link_xml, self.__report_elements)


            calculation_network = None
            definition_network = None

            # parse the component
            component = PyBRComponent.from_xml(component_xml, presentation_network, calculation_network, definition_network)
            components.append(component)

        return components
        
    def get_filing_type(self) -> str:
        """
        Get the filing type. Returns "XML".
        """
        return self.__filing_type
    
        
