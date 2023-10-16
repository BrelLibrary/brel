import lxml
import lxml.etree
from pybr import PyBRPeriod, PyBREntity, PyBRDimension, PyBRAspect

class PyBRContext:
    """
    Class for representing an XBRL context.
    an XBRL context is a collection of aspects.
    There are 5 types of aspects: concept, period, entity, unit and additional dimensions.
    The only required aspect is the concept
    """

    def __init__(self, context_id, aspects: list[PyBRAspect]) -> None:
        self.__id : str = context_id

        # aspects are the axis, characteristics are the values per axis
        self.__aspects : list[PyBRAspect] = aspects
        self.__characteristics = {}

        self.__aspects.sort(key=lambda aspect: aspect.get_name())
    
    # str getid
    # list[aspect] getaspects
    # str getvalueasstring(aspect)
    # ...
    # QName getValueAsQName(aspect)

    def get_id(self) -> str:
        """
        Get the id of the context.
        """
        return self.__id
    
    def get_aspects(self) -> list[PyBRAspect]:
        """
        Get the aspects of the context.
        """
        return self.__aspects

    def add_aspect_value(self, aspect, value) -> None:
        """
        Add an aspect to the context.
        """
        if aspect not in self.__aspects:
            # print("Warning: aspect already exists in context")
            self.__aspects.append(aspect)

            self.__characteristics[aspect] = value

            self.__aspects.sort(key=lambda aspect: aspect.get_name())
        else:
            print("asdfasdf")
        
    
    def get_value_as_object(self, aspect: PyBRAspect) -> object:
        if aspect not in self.__characteristics:
            # print("Warning: aspect not in context")
            pass
            return None
        return self.__characteristics[aspect]

    
    def __str__(self) -> str:
        output = ""
        for aspect in self.__aspects:
            output += f"{aspect} "
        return output
    
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element) -> "PyBRContext":
        """
        Creates a PyBRContext from an lxml.etree._Element.
        """
        context_id = xml_element.attrib["id"]

        context_period = xml_element.find("{*}period", namespaces=None)
        context_entity = xml_element.find("{*}entity", namespaces=None)

        context = cls(context_id, [])

        context.add_aspect_value(PyBRAspect.PERIOD, PyBRPeriod.from_xml(context_period))
        context.add_aspect_value(PyBRAspect.ENTITY, PyBREntity.from_xml(context_entity))

        # add the dimensions. the dimensions are the children of context/entity/segment
        if context_entity.find("{*}segment") is not None:
            for xml_dimension in context_entity.find("{*}segment").getchildren():
                dimension = PyBRDimension.from_xml(xml_dimension)
                context.add_aspect_value(dimension.get_aspect(), dimension)
        
        return context
