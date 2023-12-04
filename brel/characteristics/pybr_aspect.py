# from pybr import pybr_label, qname
from brel import BrelLabel, QName

class Aspect:
    """
    Base class for all aspects.
    An aspect contains a type and a value.
    The 5 base types of aspects are: concept, period, entity, unit and additional dimensions.
    Additional dimensions are not a type, but basically allow for defining additional types
    """
    # TODO: add an aspect cache

    CONCEPT: 'Aspect'
    PERIOD: 'Aspect' 
    ENTITY: 'Aspect' 
    UNIT: 'Aspect'
    LANGUAGE: 'Aspect' 

    def __init__(self, name: str, labels: list[BrelLabel]) -> None:
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
    
    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the aspect.
        """
        return self.__labels
    
    def __hash__(self) -> int:
        return hash(self.__name)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Aspect):
            return self.__name == __value.get_name()
        return False
    
    # second class citizens
    def __str__(self) -> str:
        return self.__name
    
    # internal methods
    @classmethod
    def from_QName(cls, qname: QName) -> "Aspect":
        return cls(qname.get(), [])

# initialize the core aspects
concept_labels = [
    BrelLabel("Concept [Axis]", "concept", "en-US"),
    BrelLabel("Konzept [Achse]", "concept", "de-DE"),
    BrelLabel("Concepto [Eje]", "concept", "es-ES")
]

period_labels = [
    BrelLabel("Period [Axis]", "period", "en-US"),
    BrelLabel("Periode [Achse]", "period", "de-DE"),
    BrelLabel("Periodo [Eje]", "period", "es-ES")
]

entity_labels = [
    BrelLabel("Entity [Axis]", "entity", "en-US"),
    BrelLabel("Organisation [Achse]", "entity", "de-DE"),
    BrelLabel("Entidad [Eje]", "entity", "es-ES")
]

unit_labels = [
    BrelLabel("Unit [Axis]", "unit", "en-US"),
    BrelLabel("Einheit [Achse]", "unit", "de-DE"),
    BrelLabel("Unidad [Eje]", "unit", "es-ES")
]

language_labels = [
    BrelLabel("Language [Axis]", "language", "en-US"),
    BrelLabel("Sprache [Achse]", "language", "de-DE"),
    BrelLabel("Lengua [Eje]", "language", "es-ES")
]

Aspect.CONCEPT = Aspect("concept", concept_labels)
Aspect.PERIOD = Aspect("period", period_labels)
Aspect.ENTITY = Aspect("entity", entity_labels)
Aspect.UNIT = Aspect("unit", unit_labels)
Aspect.LANGUAGE = Aspect("language", language_labels)

true_func = lambda: True

Aspect.CONCEPT.is_core = true_func
Aspect.PERIOD.is_core = true_func
Aspect.ENTITY.is_core = true_func
Aspect.UNIT.is_core = true_func
Aspect.LANGUAGE.is_core = true_func