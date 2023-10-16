from pybr import PyBRLabel

class PyBRAspect:
    """
    Base class for all aspects.
    An aspect contains a type and a value.
    The 5 base types of aspects are: concept, period, entity, unit and additional dimensions.
    Additional dimensions are not a type, but basically allow for defining additional types
    """

    CONCEPT: 'PyBRAspect'
    PERIOD: 'PyBRAspect' 
    ENTITY: 'PyBRAspect' 
    UNIT: 'PyBRAspect'
    LANGUAGE: 'PyBRAspect' 

    def __init__(self, name: str, labels: list[PyBRLabel]) -> None:
        self.__name = name
        self.__labels = labels

    def get_name(self) -> str:
        """
        Get the name of the aspect.
        """
        return self.__name
    
    def get_labels(self) -> list[PyBRLabel]:
        """
        Get the labels of the aspect.
        """
        return self.__labels
    
    def __str__(self) -> str:
        return self.__name
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PyBRAspect):
            return self.__name == __value.get_name()
        return False
    
    def __hash__(self) -> int:
        return hash(self.__name)
    
    def is_core(self) -> bool:
        """
        Check if the aspect is a core aspect.
        """
        return False
    
PyBRAspect.CONCEPT = PyBRAspect("concept", [PyBRLabel("Concept [Axis]")])
PyBRAspect.PERIOD = PyBRAspect("period", [PyBRLabel("Period [Axis]")])
PyBRAspect.ENTITY = PyBRAspect("entity", [PyBRLabel("Entity [Axis]")])
PyBRAspect.UNIT = PyBRAspect("unit", [PyBRLabel("Unit [Axis]")])
PyBRAspect.LANGUAGE = PyBRAspect("language", [PyBRLabel("Language [Axis]")])

true_func = lambda: True

PyBRAspect.CONCEPT.is_core = true_func
PyBRAspect.PERIOD.is_core = true_func
PyBRAspect.ENTITY.is_core = true_func
PyBRAspect.UNIT.is_core = true_func
PyBRAspect.LANGUAGE.is_core = true_func