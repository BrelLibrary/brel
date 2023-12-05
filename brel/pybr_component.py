from __future__ import annotations
import lxml
import lxml.etree
from .qname import QName
from .networks import PresentationNetwork, CalculationNetwork, DefinitionNetwork

class Component:
    """
    Implements XBRL components, which are sometimes also called roles.
    Components are used to define the presentation, calculation and definition networks of a filing.
    Intuitively, they function as the chapters of a report or filing.
    """

    def __init__(
            self, uri: str, info: str, 
            presentation_network: None|PresentationNetwork = None, 
            calculation_network: None|CalculationNetwork = None, 
            definition_network: None|DefinitionNetwork = None
            ) -> None:

        self.__uri = uri
        self.__info = info
        self.__presentation_network = presentation_network
        self.__calculation_network = calculation_network
        self.__definition_network = definition_network
    
    # first class citizens
    def get_URI(self) -> str:
        """
        @returns str: the URI of the component
        """
        return self.__uri

    def get_info(self) -> str:
        """
        @returns str: the info/definition of the component.
        """
        return self.__info

    def get_presentation(self) -> PresentationNetwork | None:
        """
        @returns PresentationNetwork: the presentation network of the component. None if the component has no presentation network or if the network is empty.
        """
        return self.__presentation_network

    def get_calculation(self) -> CalculationNetwork | None:
        """
        @returns CalculationNetwork: the calculation network of the component. None if the component has no calculation network or if the network is empty.
        """
        return self.__calculation_network

    def get_definition(self) -> DefinitionNetwork | None:
        """
        @returns DefinitionNetwork: the definition network of the component. None if the component has no definition network or if the network is empty.
        """
        return self.__definition_network
    
    # second class citizens
    def has_presentation(self) -> bool:
        """
        @returns bool: True if the component has a presentation network, False otherwise
        """
        return self.__presentation_network != None
    
    def has_calculation(self) -> bool:
        """
        @returns bool: True if the component has a calculation network, False otherwise
        """
        return self.__calculation_network != None

    def has_definition(self) -> bool:
        """
        @returns bool: True if the component has a definition network, False otherwise
        """
        return self.__info != ""

    def __str__(self) -> str:
        """
        @returns str: a string representation of the component
        """
        return f"Component(id='{self.__uri}', definition='{self.__info}', presentation_network={self.__presentation_network}, calculation_network={self.__calculation_network}, definition_network={self.__definition_network})"


    # internal methods
    @classmethod
    def from_xml(
        cls, 
        xml_element: lxml.etree._Element, 
        presentation_network: None|PresentationNetwork = None, 
        calculation_network: None|CalculationNetwork = None, 
        definition_network: None|DefinitionNetwork = None
    ) -> Component:
        """
        Create a Component from an lxml.etree._Element.
        """
        
        uri = xml_element.get("roleURI", None)
        nsmap = QName.get_nsmap()

        if uri is None:
            raise ValueError("The roleURI attribute is missing from the link:roleType element")

        # the info is in a child element of the xml_element called "definition"
        try:
            info_element = xml_element.find("link:definition", namespaces=nsmap)
            if info_element is None:
                info = ""
            else:
                info = info_element.text or ""
        except AttributeError:
            info = ""

        # check the usedOn elements
        used_ons = [used_on.text for used_on in xml_element.findall("link:usedOn", namespaces=nsmap)]
        if presentation_network is not None and "link:presentationLink" not in used_ons:
            raise ValueError(f"A presentation network is not allowed for the component with id '{uri}', but one was passed.")
        if calculation_network is not None and "link:calculationLink" not in used_ons:
            raise ValueError(f"A calculation network is not allowed for the component with id '{uri}', but one was passed.")
        if definition_network is not None and "link:definitionLink" not in used_ons:
            raise ValueError(f"A definition network is not allowed for the component with id '{uri}', but one was passed.")
        
        return cls(uri, info, presentation_network, calculation_network, definition_network)