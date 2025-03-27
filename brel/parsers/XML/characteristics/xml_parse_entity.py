"""
This module contains the function to parse an EntityCharacteristic from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.1
- date: 20 December 2023

====================
"""

from typing import Callable, cast

import lxml.etree

from brel.characteristics import Aspect, EntityCharacteristic, ICharacteristic


def parse_entity_from_xml(
    xml_element: lxml.etree._Element,
    get_from_cache: Callable[[str], ICharacteristic | Aspect | None],
    add_to_cache: Callable[[str, ICharacteristic | Aspect], None],
) -> EntityCharacteristic:
    """
    Create a Entity from an lxml.etree._Element.
    This is used for parsing characteristcs from an XBRL instance in XML format.
    :param xml_element: the lxml.etree._Element from which the EntityCharacteristic is created
    :param make_qname: the function to make a QName from a string
    :param get_from_cache: the function to get a characteristic from the characteristics cache
    :param add_to_cache: the function to add a characteristic to the characteristics cache
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
    entity_characteristic = get_from_cache(f"entity {entity_id}")
    if entity_characteristic is not None:
        # if the entity characteristic is already in the cache, typecheck it and return it
        if not isinstance(entity_characteristic, EntityCharacteristic):
            raise ValueError("Entity characteristic is not an entity characteristic")
        return cast(EntityCharacteristic, entity_characteristic)
    else:
        # if the entity characteristic is not in the cache, create it and add it to the cache
        entity_url = entity_id_elem.get("scheme")
        # The scheme is required by the XBRL 2.1 spec
        entity_url = cast(str, entity_url)

        # entity_qname = make_qname(f"{entity_prefix}:{entity_id}")
        entity_characteristic = EntityCharacteristic(entity_id, entity_url)
        add_to_cache(f"entity {entity_id}", entity_characteristic)
        return entity_characteristic
