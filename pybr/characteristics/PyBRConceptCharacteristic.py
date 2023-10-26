import lxml
import lxml.etree
from pybr import PyBRAspect, QName, PyBRLabel
from pybr.characteristics import PyBRICharacteristic
from pybr.reportelements import PyBRConcept

class PyBRConceptCharacteristic(PyBRICharacteristic):
    """
    Class for representing an XBRL concept.
    A contains the following information:
    - id: str. The concept's id.
    - abstract: bool. Whether the concept is abstract or not.
    - name: str. The concept's name.
    - nillable: bool. Whether the concept is nillable or not.
    - substitution_group: str. The concept's substitution group.
    - type: str. The concept's type. Used for validation.
    - period_type: str. The concept's period type. Used for validation.
    """
    # TODO: create a class called PyBRReportElement. PyBRConcept should inherit from it.

    __concept_cache: dict[QName, "PyBRConceptCharacteristic"] = {}

    def __init__(self, concept: PyBRConcept) -> None:
        self.__concept : PyBRConcept = concept
        
        self.__concept_cache[concept.get_name()] = self

    def __str__(self) -> str:
        return self.__concept.get_name().__str__()
    
    def get_value(self) -> PyBRConcept:
        return self.__concept
    
    def get_aspect(self) -> PyBRAspect:
        return PyBRAspect.CONCEPT
    
    def get_id(self) -> str:
        """
        Returns the concept's id.
        """
        # TODO: implement and ask ghislain if this is not an implementation detail
        raise NotImplementedError
    
