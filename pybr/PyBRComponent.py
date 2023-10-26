from __future__ import annotations
import lxml
import lxml.etree
from pybr import PyBRLabel, QName

class PyBRPresentationGraph:
    pass

class PyBRCalculationGraph:
    pass

class PyBRDefinitionGraph:
    pass

class PyBRComponent:
    """
    Implements XBRL components (also called roles)
    A role has a definition (essentially a name) associated labels, an ID, and maybe a presentation- calculation- and definition-graph  
    """

    def __init__(
            self, id: str, info: str, labels: list[PyBRLabel], 
            presentation_graph: None|"PyBRPresentationGraph" = None, 
            calculation_graph: None|"PyBRCalculationGraph" = None, 
            definition_graph: None|"PyBRDefinitionGraph" = None
            ) -> None:
        self.__id = id
        self.__info = info
        self.__labels = labels
        self.__presentation_graph = presentation_graph
        self.__calculation_graph = calculation_graph
        self.__definition_graph = definition_graph
    
    # first class citizens
    def get_id(self) -> str:
        """Get the ID of the component"""
        return self.__id

    def get_info(self) -> str:
        """Get the definition of the component"""
        return self.__info

    def get_labels(self) -> list[PyBRLabel]:
        """Get the labels of the component"""
        return self.__labels

    def get_presentation(self) -> "PyBRPresentationGraph" | None:
        """Get the presentation graph of the component"""
        return self.__presentation_graph

    def get_calculation(self) -> "PyBRCalculationGraph" | None:
        """Get the calculation graph of the component"""
        return self.__calculation_graph

    def get_definition(self) -> "PyBRDefinitionGraph" | None:
        """Get the definition graph of the component"""
        return self.__definition_graph
    
    # second class citizens
    def has_presentation(self) -> bool:
        """Check if the component has a presentation graph"""
        return self.__presentation_graph != None
    
    def has_calculation(self) -> bool:
        """Check if the component has a calculation graph"""
        return self.__calculation_graph != None

    def has_definition(self) -> bool:
        """Check if the component has a definition graph"""
        return self.__info != ""

    def __str__(self) -> str:
        """Get a string representation of the component"""
        return f"PyBRComponent(id='{self.__id}', definition='{self.__info}', labels={self.__labels}, presentation_graph={self.__presentation_graph}, calculation_graph={self.__calculation_graph}, definition_graph={self.__definition_graph})"


    # internal methods
    @classmethod
    def from_xml(
        cls, 
        xml_element: lxml.etree._Element, 
        labels: list[PyBRLabel],
        presentation_graph: None|"PyBRPresentationGraph" = None, 
        calculation_graph: None|"PyBRCalculationGraph" = None, 
        definition_graph: None|"PyBRDefinitionGraph" = None
    ) -> PyBRComponent:
        """
        Create a PyBRComponent from an lxml.etree._Element.
        """
        
        id = xml_element.attrib["id"]
        nsmap = QName.get_nsmap()

        # the info is in a child element of the xml_element called "definition"
        try:
            info = xml_element.find("link:definition", namespaces=nsmap).text
        except AttributeError:
            info = ""
        # info = xml_element.find("link:definition", namespaces=nsmap).text

        return cls(id, info, labels, presentation_graph, calculation_graph, definition_graph)