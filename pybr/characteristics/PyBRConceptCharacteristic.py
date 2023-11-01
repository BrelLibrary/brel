import lxml
import lxml.etree
from pybr import PyBRAspect, QName, PyBRLabel
from pybr.characteristics import PyBRICharacteristic
from pybr.reportelements import PyBRConcept

class PyBRConceptCharacteristic(PyBRICharacteristic):
    """
    Class for representing a concept characteristic.
    This class links a fact to a concept report element.
    """
    # TODO: ask ghislain if get_id() is an implementation detail or not

    __concept_cache: dict[QName, "PyBRConceptCharacteristic"] = {}

    def __init__(self, concept: PyBRConcept) -> None:
        """
        Create a PyBRConceptCharacteristic.
        @param concept: the concept of the characteristic
        @returns PyBRConceptCharacteristic: the PyBRConceptCharacteristic
        @raises ValueError: if concept is not a PyBRConcept instance
        """
        # check if the concept is actually a PyBRConcept instance
        if not isinstance(concept, PyBRConcept):
            raise ValueError(f"concept is not a PyBRConcept instance: {concept}")

        self.__concept : PyBRConcept = concept
        self.__concept_cache[concept.get_name()] = self

    def __str__(self) -> str:
        """
        Returns the name of the concept.
        @returns str: the name of the concept
        """
        return self.__concept.get_name().__str__()
    
    def get_value(self) -> PyBRConcept:
        """
        Returns the concept of the characteristic.
        @returns PyBRConcept: the concept of the characteristic
        """
        return self.__concept
    
    def get_aspect(self) -> PyBRAspect:
        """
        Returns the aspect of the characteristic. This is always PyBRAspect.CONCEPT.
        @returns PyBRAspect: the aspect of the characteristic
        """

        return PyBRAspect.CONCEPT
    
    def get_id(self) -> str:
        """
        Returns the concept's id.
        @returns str: the concept's id
        """
        raise NotImplementedError
    
