from __future__ import annotations
import lxml
import lxml.etree
from .qname import QName
from .networks import PresentationNetwork, CalculationNetwork, DefinitionNetwork

class PyBRComponent:
    """
    Implements XBRL components (also called roles)
    A role has a definition (essentially a name), an ID, and maybe a presentation- calculation- and definition-network
    TODO: update docstring
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
        """Get the ID of the component"""
        return self.__uri

    def get_info(self) -> str:
        """Get the definition of the component"""
        return self.__info

    def get_presentation(self) -> PresentationNetwork | None:
        """Get the presentation graph of the component"""
        return self.__presentation_network

    def get_calculation(self) -> CalculationNetwork|None:
        """Get the calculation graph of the component"""
        return self.__calculation_network

    def get_definition(self) -> DefinitionNetwork | None:
        """Get the definition graph of the component"""
        return self.__definition_network
    
    # second class citizens
    def has_presentation(self) -> bool:
        """Check if the component has a presentation graph"""
        return self.__presentation_network != None
    
    def has_calculation(self) -> bool:
        """Check if the component has a calculation graph"""
        return self.__calculation_network != None

    def has_definition(self) -> bool:
        """Check if the component has a definition graph"""
        return self.__info != ""

    def __str__(self) -> str:
        """Get a string representation of the component"""
        return f"PyBRComponent(id='{self.__uri}', definition='{self.__info}', presentation_graph={self.__presentation_network}, calculation_graph={self.__calculation_network}, definition_graph={self.__definition_network})"


    # internal methods
    @classmethod
    def from_xml(
        cls, 
        xml_element: lxml.etree._Element, 
        presentation_network: None|PresentationNetwork = None, 
        calculation_network: None|CalculationNetwork = None, 
        definition_graph: None|DefinitionNetwork = None
    ) -> PyBRComponent:
        """
        Create a PyBRComponent from an lxml.etree._Element.
        """

        # TODO: use the "usedOn" information in the xml to check if the correct networks are being passed
        
        uri = xml_element.get("roleURI", None)
        nsmap = QName.get_nsmap()

        if uri is None:
            raise ValueError("The roleURI attribute is missing from the link:roleType element")

        # the info is in a child element of the xml_element called "definition"
        try:
            info = xml_element.find("link:definition", namespaces=nsmap).text
        except AttributeError:
            info = ""

        # # check the usedOn elements
        # for used_on in xml_element.findall("link:usedOn", namespaces=nsmap):
        #     # get the text of the element
        #     # if there is a presentationLink text, make sure that a presentation network is passed
        #     if used_on.text == "link:presentationLink" and presentation_network is None:
        #         raise ValueError(f"A presentation network is required for the component with id '{uri}'")
        #     elif used_on.text == "link:calculationsLink" and len(calculation_networks) == 0:
        #         raise ValueError(f"A calculation network is required for the component with id '{uri}'")
        #     elif used_on.text == "link:definitionLink" and definition_graph is None:
        #         # TODO: uncomment this as soon as the definition graph is implemented
        #         # raise ValueError("A definition graph is required for this component")
        #         pass
                

        return cls(uri, info, presentation_network, calculation_network, definition_graph)