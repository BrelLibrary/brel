import lxml
import lxml.etree
from pybr import PyBRPeriodCharacteristic, PyBREntityCharacteristic, PyBRExplicitDimensionCharacteristic, PyBRAspect, QName
from pybr.characteristics import PyBRICharacteristic
from pybr.reportelements import IReportElement, PyBRDimension, PyBRMember
from typing import cast

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

    def add_characteristic(self, aspect: PyBRAspect, value: PyBRICharacteristic) -> None:
        """
        Add an aspect to the context.
        """
        if aspect not in self.__aspects:
            # print("Warning: aspect already exists in context")
            self.__aspects.append(aspect)

            self.__characteristics[aspect] = value

            self.__aspects.sort(key=lambda aspect: aspect.get_name())
        else:
            pass
    
    def get_characteristic(self, aspect: PyBRAspect) -> PyBRICharacteristic | None:
        """
        Get the value of an aspect.
        """
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
    def from_xml(cls, xml_element: lxml.etree._Element, report_elements: dict[QName, IReportElement]) -> "PyBRContext":
        """
        Creates a PyBRContext from an lxml.etree._Element.
        @param xml_element: lxml.etree._Element. The lxml.etree._Element to create the PyBRContext from.
        @param report_elements: list[IReportElement]. The report elements to use for the context. If the context contains a dimension, then both the dimension and the member must be in the report elements.
        """
        context_id = xml_element.attrib["id"]

        context_period = xml_element.find("{*}period", namespaces=None)
        context_entity = xml_element.find("{*}entity", namespaces=None)

        context = cls(context_id, [])

        context.add_characteristic(PyBRAspect.PERIOD, PyBRPeriodCharacteristic.from_xml(context_period))
        context.add_characteristic(PyBRAspect.ENTITY, PyBREntityCharacteristic.from_xml(context_entity))

        # add the dimensions. the dimensions are the children of context/entity/segment
        if context_entity.find("{*}segment") is not None:
            for xml_dimension in context_entity.find("{*}segment").getchildren():
                dimension_axis = QName.from_string(xml_dimension.get("dimension"))
                dimension_value = QName.from_string(xml_dimension.text)

                dimension = cast(PyBRDimension, report_elements.get(dimension_axis))
                member = cast(PyBRMember, report_elements.get(dimension_value)) 

                # make sure the member and dimension are in the report elements
                if dimension is None or member is None:
                    raise ValueError("Dimension or member not found in report elements. Please make sure that the dimension and member are in the report elements.")
                
                # also make sure that they are PyBRDimension and PyBRMember instances
                if not isinstance(dimension, PyBRDimension) or not isinstance(member, PyBRMember):
                    raise ValueError("Dimension or member not found in report elements. Please make sure that the dimension and member are in the report elements.")

                dimension_characteristic = PyBRExplicitDimensionCharacteristic.from_xml(xml_dimension, dimension, member)
                context.add_characteristic(dimension_characteristic.get_aspect(), dimension_characteristic)
        
        return context
