"""
Contains the BrelAspect class.

@author: Robin Schmidiger
@version: 0.1
@date: 2023-12-19
"""

from brel import BrelLabel, QName

class BrelAspect:
    """
    Base class for all aspects.
    An aspect contains a type and a value.
    The 5 base types of aspects are: concept, period, entity, unit and additional dimensions.
    Additional dimensions are not a type, but basically allow for defining additional types
    """

    CONCEPT: 'BrelAspect'
    PERIOD: 'BrelAspect' 
    ENTITY: 'BrelAspect' 
    UNIT: 'BrelAspect'
    LANGUAGE: 'BrelAspect' 

    __aspect_cache: dict[str, 'BrelAspect'] = {}

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
        if isinstance(__value, BrelAspect):
            return self.__name == __value.get_name()
        return False
    
    # second class citizens
    def __str__(self) -> str:
        return self.__name
    
    # internal methods
    @classmethod
    def from_QName(cls, qname: QName, labels: list[BrelLabel] | None = None) -> "BrelAspect":
        """
        Creates a new aspect from a QName.
        :param qname: the QName to create the aspect from
        :param labels: A list of labels for the aspect. If None, an empty list is used.
        """
        qname_str = qname.get()
        return cls.from_str(qname_str, labels)
    
    @classmethod
    def from_str(cls, name: str, labels: list[BrelLabel] | None = None) -> "BrelAspect":
        """
        Creates a new aspect from a string.
        :param name: the string to create the aspect from
        :param labels: A list of labels for the aspect. If None, an empty list is used.
        """
        if name in cls.__aspect_cache:
            return cls.__aspect_cache[name]
        
        if labels is None:
            labels = []

        return cls(name, labels)

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

BrelAspect.CONCEPT = BrelAspect("concept", concept_labels)
BrelAspect.PERIOD = BrelAspect("period", period_labels)
BrelAspect.ENTITY = BrelAspect("entity", entity_labels)
BrelAspect.UNIT = BrelAspect("unit", unit_labels)
BrelAspect.LANGUAGE = BrelAspect("language", language_labels)

def true_func() -> bool:
    return True

BrelAspect.CONCEPT.is_core = true_func
BrelAspect.PERIOD.is_core = true_func
BrelAspect.ENTITY.is_core = true_func
BrelAspect.UNIT.is_core = true_func
BrelAspect.LANGUAGE.is_core = true_func