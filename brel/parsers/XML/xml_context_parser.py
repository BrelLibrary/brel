"""
This module contains the function to parse the contexts from the xbrl instance.
It parses XBRL in the XML syntax.
It only parses the syntactic context, therefore the Unit and Concept characteristics are not parsed and must be provided as arguments.

@author: Robin Schmidiger
@version: 0.1
@date: 13 December 2023
"""

import lxml.etree
from brel import QName, QNameNSMap, Context
from brel.characteristics import *
from brel.reportelements import *

from typing import cast

def parse_context_xml( 
        xml_element: lxml.etree._Element, 
        characteristics: list[UnitCharacteristic | ConceptCharacteristic], 
        report_elements: dict[QName, IReportElement],
        qname_nsmap: QNameNSMap
        ) -> "Context":
    """
    Creates a Context from an lxml.etree._Element.
    @param xml_element: lxml.etree._Element. The lxml.etree._Element to create the Context from.
    @param report_elements: list[IReportElement]. The report elements to use for the context. If the context contains a dimension, then both the dimension and the member must be in the report elements.
    """

    context_id = xml_element.attrib["id"]

    # check if the supplied list of characteristics only contains units and concepts
    for characteristic in characteristics:
        if not isinstance(characteristic, UnitCharacteristic) and not isinstance(characteristic, ConceptCharacteristic):
            raise ValueError(f"Context id {context_id} contains a characteristic that is not a unit or a concept. Please make sure that the list of characteristics only contains units and concepts.")

    context_period = xml_element.find("{*}period", namespaces=None)
    context_entity = xml_element.find("{*}entity", namespaces=None)

    if context_period is None:
        raise ValueError(f"Context id {context_id!r} does not contain a period. Please make sure that the context contains a period.")
    
    if context_entity is None:
        raise ValueError(f"Context id {context_id!r} does not contain an entity. Please make sure that the context contains an entity.")

    context = Context(context_id, [])

    # add the characteristics provided by the user. these are the unit and concept
    for characteristic in characteristics:
        context._add_characteristic(characteristic)


    context._add_characteristic(PeriodCharacteristic.from_xml(context_period, qname_nsmap))
    context._add_characteristic(EntityCharacteristic.from_xml(context_entity, qname_nsmap))

    # add the dimensions. the dimensions are the children of context/entity/segment
    segment = context_entity.find("{*}segment", namespaces=None)

    if segment is not None:
        for xml_dimension in segment:
            # if it is an explicit dimension, the tag is xbrli:explicitMember
            if "explicitMember" in xml_dimension.tag: 

                # get the dimension
                dimension_axis_str = xml_dimension.get("dimension")
                if dimension_axis_str is None:
                    raise ValueError(f"Dimension attribute not found in xml element. Please make sure that the dimension attribute is in the xml element. {xml_dimension}")

                dimension_axis = QName.from_string(dimension_axis_str, qname_nsmap)
                dimension = cast(Dimension, report_elements.get(dimension_axis))

                # get the member
                dimension_value_str = xml_dimension.text
                if dimension_value_str is None:
                    raise ValueError(f"Dimension value not found in xml element. Please make sure that the dimension value is in the xml element. {xml_dimension}")
                
                dimension_value = QName.from_string(dimension_value_str, qname_nsmap)
                member = cast(Member, report_elements.get(dimension_value)) 

                # make sure the member and dimension are in the report elements
                if dimension is None or member is None:
                    raise ValueError(f"Dimension or member not found in report elements. Please make sure that the dimension and member are in the report elements. {dimension} {member}")
                
                # also make sure that they are Dimension and Member instances
                if not isinstance(dimension, Dimension) or not isinstance(member, Member):
                    print(dimension, member)
                    raise ValueError("Dimension or member not found in report elements. Please make sure that the dimension and member are in the report elements.")
                
                # create and add the characteristic
                dimension_characteristic: ICharacteristic = ExplicitDimensionCharacteristic.from_xml(xml_dimension, dimension, member, qname_nsmap)
                context._add_characteristic(dimension_characteristic)
            # if it is a typed dimension, the tag is xbrli:typedMember
            elif "typedMember" in xml_dimension.tag:

                # get the dimension
                dimension_axis_str = xml_dimension.get("dimension")
                if dimension_axis_str is None:
                    raise ValueError(f"Dimension attribute not found in xml element. Please make sure that the dimension attribute is in the xml element. {xml_dimension}")
                
                dimension_axis = QName.from_string(dimension_axis_str, qname_nsmap)
                dimension = cast(Dimension, report_elements.get(dimension_axis))

                # get the value from the xml element
                # TODO: parse the value as a type instead of just getting the text as a str
                dimension_value = xml_dimension.getchildren()[0].text

                # make sure the dimension is in the report elements
                if dimension is None:
                    raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")
                
                # also make sure that it is a Dimension instance
                if not isinstance(dimension, Dimension):
                    raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")
                
                # create and add the characteristic
                dimension_characteristic = TypedDimensionCharacteristic.from_xml(xml_dimension, dimension, dimension_value)
                context._add_characteristic(dimension_characteristic)
            else:
                raise ValueError(f"Unknown dimension type {xml_dimension.tag}. Please make sure that the dimension is either an explicitMember or a typedMember. {xml_dimension.tag}")
    
    return context