import lxml
import lxml.etree
# from pybr import PyBRPeriodCharacteristic, PyBREntityCharacteristic, PyBRExplicitDimensionCharacteristic, PyBRTypedDimensionCharacteristic, PyBRAspect, QName
from .characteristics.pybr_aspect import PyBRAspect
from .qname import QName
# from .characteristics import concept_characteristic, entity_characteristic, i_characteristic, period_characteristic, unit_characteristic
# from .characteristics import 
from .characteristics.concept_characteristic import PyBRConceptCharacteristic
from .characteristics.i_characteristic import PyBRICharacteristic
from .characteristics.entity_characteristic import PyBREntityCharacteristic
from .characteristics.period_characteristic import PyBRPeriodCharacteristic
from .characteristics.unit_characteristic import PyBRUnitCharacteristic
from .characteristics.typed_dimension_characteristic import PyBRTypedDimensionCharacteristic
from .characteristics.explicit_dimension_characteristic import PyBRExplicitDimensionCharacteristic
from .reportelements import PyBRDimension, PyBRMember, IReportElement
from typing import cast

class PyBRContext:
    """
    Class for representing an XBRL context.
    an XBRL context is a collection of aspects.
    There are 5 types of aspects: concept, period, entity, unit and additional dimensions.
    The only required aspect is the concept
    """
    # TODO: implement second class citizens

    def __init__(self, context_id, aspects: list[PyBRAspect]) -> None:
        self.__id : str = context_id

        # aspects are the axis, characteristics are the values per axis
        self.__aspects : list[PyBRAspect] = aspects
        self.__characteristics = {}

        self.__aspects.sort(key=lambda aspect: aspect.get_name())
    
    # First class citizens
    def get_aspects(self) -> list[PyBRAspect]:
        """
        Get the aspects of the context.
        """
        return self.__aspects
    
    def get_characteristic(self, aspect: PyBRAspect) -> PyBRICharacteristic | None:
        """
        Get the value of an aspect.
        """
        if aspect not in self.__characteristics:
            pass
            return None
        return self.__characteristics[aspect]
    
    # Second class citizens
    def has_characteristic(self, aspect: PyBRAspect) -> bool:
        raise NotImplementedError()
    
    def get_characteristic_as_str(self, aspect: PyBRAspect) -> str:
        raise NotImplementedError()
    
    def get_characteristic_as_qname(self, aspect: PyBRAspect) -> QName:
        raise NotImplementedError()
    
    def get_characteristic_as_int(self, aspect: PyBRAspect) -> int:
        raise NotImplementedError()
    
    def get_characteristic_as_float(self, aspect: PyBRAspect) -> float:
        raise NotImplementedError()
    
    def get_characteristic_as_bool(self, aspect: PyBRAspect) -> bool:
        raise NotImplementedError()
    
    def get_concept(self) -> PyBRConceptCharacteristic:
        raise NotImplementedError()
    
    def get_period(self) -> PyBRPeriodCharacteristic | None:
        raise NotImplementedError()
    
    def get_entity(self) -> PyBREntityCharacteristic | None:
        raise NotImplementedError()
    
    def get_unit(self) -> PyBRUnitCharacteristic | None:
        raise NotImplementedError()

    # Internal methods
    def __add_characteristic(self, characteristic: PyBRICharacteristic) -> None:
        """
        Add an aspect to the context.
        """
        aspect = characteristic.get_aspect()

        if aspect not in self.__aspects:
            self.__aspects.append(aspect)

            self.__characteristics[aspect] = characteristic

            self.__aspects.sort(key=lambda aspect: aspect.get_name())
        else:
            pass
    
    def _get_id(self) -> str:
        """
        Get the id of the context.
        This is an implementation detail of the underlying XBRL library.
        It serves as a good sanity check 
        """
        return self.__id
    
    def __str__(self) -> str:
        output = ""
        for aspect in self.__aspects:
            output += f"{aspect} "
        return output
    
    @classmethod
    def from_xml(cls, xml_element: lxml.etree._Element, characteristics: list[PyBRUnitCharacteristic | PyBRConceptCharacteristic], report_elements: dict[QName, IReportElement]) -> "PyBRContext":
        """
        Creates a PyBRContext from an lxml.etree._Element.
        @param xml_element: lxml.etree._Element. The lxml.etree._Element to create the PyBRContext from.
        @param report_elements: list[IReportElement]. The report elements to use for the context. If the context contains a dimension, then both the dimension and the member must be in the report elements.
        """

        context_id = xml_element.attrib["id"]

        # check if the supplied list of characteristics only contains units and concepts
        for characteristic in characteristics:
            if not isinstance(characteristic, PyBRUnitCharacteristic) and not isinstance(characteristic, PyBRConceptCharacteristic):
                raise ValueError(f"Context id {context_id} contains a characteristic that is not a unit or a concept. Please make sure that the list of characteristics only contains units and concepts.")

        context_period = xml_element.find("{*}period", namespaces=None)
        context_entity = xml_element.find("{*}entity", namespaces=None)

        context = cls(context_id, [])

        # add the characteristics provided by the user. these are the unit and concept
        for characteristic in characteristics:
            context.__add_characteristic(characteristic)

        context.__add_characteristic(PyBRPeriodCharacteristic.from_xml(context_period))
        context.__add_characteristic(PyBREntityCharacteristic.from_xml(context_entity))

        # add the dimensions. the dimensions are the children of context/entity/segment
        if context_entity.find("{*}segment") is not None:
            for xml_dimension in context_entity.find("{*}segment").getchildren():
                # if it is an explicit dimension, the tag is xbrli:explicitMember
                if "explicitMember" in xml_dimension.tag: 

                    # get the dimension
                    dimension_axis = QName.from_string(xml_dimension.get("dimension"))
                    dimension = cast(PyBRDimension, report_elements.get(dimension_axis))

                    # get the member
                    dimension_value = QName.from_string(xml_dimension.text)
                    member = cast(PyBRMember, report_elements.get(dimension_value)) 

                    # make sure the member and dimension are in the report elements
                    if dimension is None or member is None:
                        print(dimension, member)
                        raise ValueError("Dimension or member not found in report elements. Please make sure that the dimension and member are in the report elements.")
                    
                    # also make sure that they are PyBRDimension and PyBRMember instances
                    if not isinstance(dimension, PyBRDimension) or not isinstance(member, PyBRMember):
                        print(dimension, member)
                        raise ValueError("Dimension or member not found in report elements. Please make sure that the dimension and member are in the report elements.")
                    
                    # create and add the characteristic
                    dimension_characteristic = PyBRExplicitDimensionCharacteristic.from_xml(xml_dimension, dimension, member)
                    context.__add_characteristic(dimension_characteristic)
                # if it is a typed dimension, the tag is xbrli:typedMember
                elif "typedMember" in xml_dimension.tag: # TODO: make this more robust

                    # get the dimension
                    dimension_axis = QName.from_string(xml_dimension.get("dimension"))
                    dimension = cast(PyBRDimension, report_elements.get(dimension_axis))

                    # get the value from the xml element
                    # TODO: parse the value as a type instead of just getting the text as a str
                    dimension_value = xml_dimension.getchildren()[0].text

                    # make sure the dimension is in the report elements
                    if dimension is None:
                        raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")
                    
                    # also make sure that it is a PyBRDimension instance
                    if not isinstance(dimension, PyBRDimension):
                        raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")
                    
                    # create and add the characteristic
                    dimension_characteristic = PyBRTypedDimensionCharacteristic.from_xml(xml_dimension, dimension, dimension_value)
                    context.__add_characteristic(dimension_characteristic)
                else:
                    raise ValueError("Unknown dimension type. Please make sure that the dimension is either an explicitMember or a typedMember.")
        
        return context
