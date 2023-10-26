from pybr import PyBRLabel, QName

class PyBRAspect:
    """
    Base class for all aspects.
    An aspect contains a type and a value.
    The 5 base types of aspects are: concept, period, entity, unit and additional dimensions.
    Additional dimensions are not a type, but basically allow for defining additional types
    """
    # TODO: add an aspect cache

    CONCEPT: 'PyBRAspect'
    PERIOD: 'PyBRAspect' 
    ENTITY: 'PyBRAspect' 
    UNIT: 'PyBRAspect'
    LANGUAGE: 'PyBRAspect' 

    def __init__(self, name: str, labels: list[PyBRLabel]) -> None:
        self.__name = name
        self.__labels = labels
    
    # first class citizens
    def get_name(self) -> str:
        """
        Get the name of the aspect.
        """
        return self.__name
    
    def is_core(self) -> bool:
        """
        Check if the aspect is a core aspect.
        """
        return False
    
    def get_labels(self) -> list[PyBRLabel]:
        """
        Get the labels of the aspect.
        """
        return self.__labels
    
    def __hash__(self) -> int:
        return hash(self.__name)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PyBRAspect):
            return self.__name == __value.get_name()
        return False
    
    # second class citizens
    def __str__(self) -> str:
        return self.__name
    
    # internal methods
    @classmethod
    def from_QName(cls, qname: QName) -> "PyBRAspect":
        return cls(qname.get(), [])

# initialize the core aspects
concept_labels = [
    PyBRLabel("Concept [Axis]", "en-US"),
    PyBRLabel("Konzept [Achse]", "de-DE"),
    PyBRLabel("Concepto [Eje]", "es-ES")
]

period_labels = [
    PyBRLabel("Period [Axis]", "en-US"),
    PyBRLabel("Periode [Achse]", "de-DE"),
    PyBRLabel("Periodo [Eje]", "es-ES")
]

entity_labels = [
    PyBRLabel("Entity [Axis]", "en-US"),
    PyBRLabel("Organisation [Achse]", "de-DE"),
    PyBRLabel("Entidad [Eje]", "es-ES")
]

unit_labels = [
    PyBRLabel("Unit [Axis]", "en-US"),
    PyBRLabel("Einheit [Achse]", "de-DE"),
    PyBRLabel("Unidad [Eje]", "es-ES")
]

language_labels = [
    PyBRLabel("Language [Axis]", "en-US"),
    PyBRLabel("Sprache [Achse]", "de-DE"),
    PyBRLabel("Lengua [Eje]", "es-ES")
]

PyBRAspect.CONCEPT = PyBRAspect("concept", concept_labels)
PyBRAspect.PERIOD = PyBRAspect("period", period_labels)
PyBRAspect.ENTITY = PyBRAspect("entity", entity_labels)
PyBRAspect.UNIT = PyBRAspect("unit", unit_labels)
PyBRAspect.LANGUAGE = PyBRAspect("language", language_labels)

true_func = lambda: True

PyBRAspect.CONCEPT.is_core = true_func
PyBRAspect.PERIOD.is_core = true_func
PyBRAspect.ENTITY.is_core = true_func
PyBRAspect.UNIT.is_core = true_func
PyBRAspect.LANGUAGE.is_core = true_func