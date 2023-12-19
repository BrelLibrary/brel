"""
This module contains the function to parse the contexts from the xbrl instance.
It parses XBRL in the XML syntax.
It only parses the syntactic context, therefore the Unit and Concept characteristics are not parsed and must be provided as arguments.

@author: Robin Schmidiger
@version: 0.1
@date: 19 December 2023
"""

import lxml.etree
from brel import QName, QNameNSMap, Context
from brel.characteristics import *
from brel.reportelements import *

from typing import cast

def parse_entity_from_xml(
    xml_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    characteristics_cache: dict[str, ICharacteristic|BrelAspect]
    ) -> EntityCharacteristic:
    """
    Create a Entity from an lxml.etree._Element.
    This is used for parsing characteristcs from an XBRL instance in XML format.
    :param xml_element: the lxml.etree._Element from which the EntityCharacteristic is created
    :returns EntityCharacteristic: the EntityCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    # first check if there is an identifier element
    identifier_element = xml_element.find("{*}identifier", namespaces=None)

    if identifier_element is None:
        raise ValueError("Could not find identifier element in entity characteristic")
    
    # then check if there is a scheme attribute
    if "scheme" not in identifier_element.attrib:
        raise ValueError("Could not find scheme attribute in identifier element")
    

    entity_id_elem = xml_element.find("{*}identifier", namespaces=None)
    # The identifier element is guaranteed according to the XBRL 2.1 specification to have a text element
    entity_id_elem = cast(lxml.etree._Element, entity_id_elem)
    entity_id = entity_id_elem.text
    # The text is guaranteed to have at least length 1 according to the XBRL 2.1 spec
    entity_id = cast(str, entity_id)

    # check the cache
    if entity_id in characteristics_cache:
        return cast(EntityCharacteristic, characteristics_cache[entity_id])

    entity_url = entity_id_elem.get("scheme")
    # The scheme is required by the XBRL 2.1 spec
    entity_url = cast(str, entity_url) 
    
    entity_prefix = QName.get_prefix_from_url(entity_url)

    if entity_prefix is None:
        raise ValueError(f"Could not find prefix for entity URL: {entity_url}")
    
    # QName.add_to_nsmap(entity_url, entity_prefix)
    qname_nsmap.add_to_nsmap(entity_url, entity_prefix)
    
    entity_qname = QName.from_string(f"{entity_prefix}:{entity_id}", qname_nsmap)

    # add the entity to the cache
    entity_characteristic = EntityCharacteristic(entity_qname)
    characteristics_cache[entity_id] = entity_characteristic
    return entity_characteristic

def parse_period_from_xml(
    xml_element: lxml.etree._Element,
    qname_nsmap: QNameNSMap,
    characteristics_cache: dict[str, ICharacteristic|BrelAspect]
    ) -> PeriodCharacteristic:
    """
    Create a Period from an lxml.etree._Element.
    :param xml_element: the lxml.etree._Element from which the PeriodCharacteristic is created
    :param qname_nsmap: the QNameNSMap
    :returns: the PeriodCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    nsmap = qname_nsmap.get_nsmap()

    is_instant = xml_element.find("{*}instant", nsmap) is not None
    if is_instant:
        instant_date_elem = xml_element.find("{*}instant", nsmap)
        if instant_date_elem is None:
            raise ValueError("Could not find instant element in period characteristic")
        instant_date = instant_date_elem.text
        if instant_date is None:
            raise ValueError("The instant element has no text")
        
        # check cache
        if instant_date in characteristics_cache:
            return cast(PeriodCharacteristic, characteristics_cache[instant_date])
        else:
            period_characteristic = PeriodCharacteristic.instant(instant_date)
            characteristics_cache[instant_date] = period_characteristic
            return period_characteristic

    else:
        start_date_elem = xml_element.find("{*}startDate", nsmap)
        if start_date_elem is None:
            raise ValueError("Could not find startDate element in period characteristic")
        start_date = start_date_elem.text
        if start_date is None:
            raise ValueError("The startDate element has no text")
        
        end_date_elem = xml_element.find("{*}endDate", nsmap)
        if end_date_elem is None:
            raise ValueError("Could not find endDate element in period characteristic")
        end_date = end_date_elem.text
        if end_date is None:
            raise ValueError("The endDate element has no text")
        
        # check cache
        if "{start_date} {end_date}" in characteristics_cache:
            return cast(PeriodCharacteristic, characteristics_cache["{start_date} {end_date}"])
        else:
            period_characteristic = PeriodCharacteristic.duration(start_date, end_date)
            characteristics_cache["{start_date} {end_date}"] = period_characteristic
            return period_characteristic

def parse_typed_dim_from_xml(
    xml_element: lxml.etree._Element,
    report_elements: dict[QName, IReportElement],
    qname_nsmap: QNameNSMap,
    characteristics_cache: dict[str, ICharacteristic|BrelAspect]
    ) -> TypedDimensionCharacteristic:
    """
    Create a Dimension from an lxml.etree._Element.
    :param xml_element: the xml subtree from which the Dimension is created
    :param report_elements: the report elements to use for the Dimension
    :param qname_nsmap: the QNameNSMap
    :characteristics_cache: the characteristics cache
    :returns ExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """

    """
    A typed dimension may look like this:
    <xbrli:typedMember dimension="us-gaap:StatementClassOfStockAxis">
        <us-gaap:StatementClassOfStockAxis.domain>us-gaap:ClassACommonStockMember</us-gaap:StatementClassOfStockAxis.domain>
    </xbrli:typedMember>
    
    The three relevant parts are:
    - the tag (xbrli:typedMember)
    - the dimension attribute, "us-gaap:StatementClassOfStockAxis" in this case
    - the value of the domain element, "us-gaap:ClassACommonStockMember" in this case
    Note that the tag us-gaap:StatementClassOfStockAxis.domain is just a dummy tag and is not used.

    From xbrli:typedMember, we know that we are dealing with a typed dimension.
    From the dimension attribute, we know which dimension we are dealing with.
    From the value of the domain element, we know which member we are dealing with.
    """

    # Get the dimension attribute from the xml element
    dimension_axis = xml_element.get("dimension")
    if dimension_axis is None:
        raise ValueError("Could not find dimension attribute in explicit dimension characteristic")
    
    # check cache for dimension aspect
    if f"aspect {dimension_axis}" in characteristics_cache:
        dimension_aspect = cast(BrelAspect, characteristics_cache[f"aspect {dimension_axis}"])
        dimension_qname: QName = QName.from_string(dimension_axis, qname_nsmap)
    else:
        dimension_qname = QName.from_string(dimension_axis, qname_nsmap)
        dimension_aspect = BrelAspect.from_QName(dimension_qname)
        characteristics_cache[f"aspect {dimension_axis}"] = dimension_aspect
    
    # get the dimension from the report elements
    if dimension_qname not in report_elements:
        raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")

    dimension = cast(Dimension, report_elements.get(dimension_qname))

    # get the dimension value from the xml element
    children = list(xml_element)
    if len(children) != 1:
        raise ValueError("Typed dimension characteristic has more than one child")
    
    value_element = children[0]
    dimension_value = value_element.text
    if dimension_value is None:
        raise ValueError("Dimension value not found in xml element. Please make sure that the dimension value is in the xml element. {xml_dimension}")
    
    # check cache
    if f"{dimension_axis} {dimension_value}" in characteristics_cache:
        return cast(TypedDimensionCharacteristic, characteristics_cache[f"{dimension_axis} {dimension_value}"])
    else:
        dimension_characteristic = TypedDimensionCharacteristic(dimension, dimension_value, dimension_aspect)
        characteristics_cache[f"{dimension_axis} {dimension_value}"] = dimension_characteristic
        return dimension_characteristic

def parse_explicit_dim_from_xml(
    xml_element: lxml.etree._Element,
    report_elements: dict[QName, IReportElement],
    qname_nsmap: QNameNSMap,
    characteristics_cache: dict[str, ICharacteristic|BrelAspect]
    ) -> ExplicitDimensionCharacteristic:
    """
    Create a Dimension from an lxml.etree._Element.
    :param xml_element: the xml subtree from which the Dimension is created
    :param report_elements: the report elements to use for the Dimension
    :param qname_nsmap: the QNameNSMap
    :characteristics_cache: the characteristics cache
    :returns ExplicitDimensionCharacteristic: the explicit dimension characteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    # get the dimension attribute from the xml element
    dimension_axis = xml_element.get("dimension")
    if dimension_axis is None:
        raise ValueError("Could not find dimension attribute in explicit dimension characteristic")
    
    # check cache for dimension aspect
    if f"aspect {dimension_axis}" in characteristics_cache:
        dimension_aspect = cast(BrelAspect, characteristics_cache[f"aspect {dimension_axis}"])
        dimension_qname: QName = QName.from_string(dimension_axis, qname_nsmap)
    else:
        dimension_qname = QName.from_string(dimension_axis, qname_nsmap)
        dimension_aspect = BrelAspect.from_QName(dimension_qname)
        characteristics_cache[f"aspect {dimension_axis}"] = dimension_aspect
    
    # get the dimension from the report elements
    if dimension_qname not in report_elements:
        raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")
    
    dimension = cast(Dimension, report_elements.get(dimension_qname))
    # check if the dimension is a Dimension instance
    if not isinstance(dimension, Dimension):
        raise ValueError("Dimension not found in report elements. Please make sure that the dimension is in the report elements.")
    
    # get the value from the xml element
    dimension_value = xml_element.text
    if dimension_value is None:
        raise ValueError("Dimension value not found in xml element. Please make sure that the dimension value is in the xml element. {xml_dimension}")
    
    # turn the value into a QName
    dimension_value_qname = QName.from_string(dimension_value, qname_nsmap)

    # get the member from the report elements
    if dimension_value_qname not in report_elements:
        raise ValueError("Member not found in report elements. Please make sure that the member is in the report elements.")
    
    member = cast(Member, report_elements.get(dimension_value_qname))
    # check if the member is a Member instance
    if not isinstance(member, Member):
        raise ValueError("Member not found in report elements. Please make sure that the member is in the report elements.")

    # check cache
    if f"{dimension_axis} {dimension_value}" in characteristics_cache:
        return cast(ExplicitDimensionCharacteristic, characteristics_cache[f"{dimension_axis} {dimension_value}"])
    else:
        # create and add the characteristic
        dimension_characteristic = ExplicitDimensionCharacteristic(dimension, member, dimension_aspect)
        characteristics_cache[f"{dimension_axis} {dimension_value}"] = dimension_characteristic
        return dimension_characteristic


def parse_context_xml( 
        xml_element: lxml.etree._Element, 
        characteristics: list[UnitCharacteristic | ConceptCharacteristic], 
        report_elements: dict[QName, IReportElement],
        qname_nsmap: QNameNSMap,
        characteristics_cache: dict[str, ICharacteristic|BrelAspect]
        ) -> "Context":
    """
    Creates a Context from an lxml.etree._Element.
    :param xml_element: lxml.etree._Element. The lxml.etree._Element to create the Context from.
    :param characteristics: list[ICharacteristic]. The characteristics to use for the context. If the context contains a dimension, then both the dimension and the member must be in the characteristics.
    :param report_elements: list[IReportElement]. The report elements to use for the context. If the context contains a dimension, then both the dimension and the member must be in the report elements.
    :param qname_nsmap: QNameNSMap. The QNameNSMap to use for the context.
    :param characteristics_cache: dict[str, ICharacteristic]. The characteristics cache to use for the context.
    :returns: Context. The context created from the lxml.etree._Element.
    :raises ValueError: if the XML element is malformed
    """

    context_id = xml_element.get("id")
    if context_id is None:
        raise ValueError("Could not find id attribute in context")

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


    context._add_characteristic(parse_period_from_xml(context_period, qname_nsmap, characteristics_cache))
    context._add_characteristic(parse_entity_from_xml(context_entity, qname_nsmap, characteristics_cache))

    # add the dimensions. the dimensions are the children of context/entity/segment
    segment = context_entity.find("{*}segment", namespaces=None)

    if segment is not None:
        for xml_dimension in segment:
            # if it is an explicit dimension, the tag is xbrli:explicitMember
            if "explicitMember" in xml_dimension.tag: 
                explicit_dimension_characteristic = parse_explicit_dim_from_xml(xml_dimension, report_elements, qname_nsmap, characteristics_cache)
                context._add_characteristic(explicit_dimension_characteristic)
            # if it is a typed dimension, the tag is xbrli:typedMember
            elif "typedMember" in xml_dimension.tag:
                typed_dimension_characteristic = parse_typed_dim_from_xml(xml_dimension, report_elements, qname_nsmap, characteristics_cache)
                context._add_characteristic(typed_dimension_characteristic)

            else:
                raise ValueError(f"Unknown dimension type {xml_dimension.tag}. Please make sure that the dimension is either an explicitMember or a typedMember. {xml_dimension.tag}")
    
    return context