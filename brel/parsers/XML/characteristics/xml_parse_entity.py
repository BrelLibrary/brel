"""
This module contains the function to parse an EntityCharacteristic from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 April 2025

====================
"""


import lxml.etree

from brel.characteristics import EntityCharacteristic
from brel.contexts.filing_context import FilingContext
from brel.data.characteristic.characteristic_repository import CharacteristicRepository
from brel.parsers.utils.error_utils import error_on_none


def parse_entity_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
) -> EntityCharacteristic:
    """
    Create a Entity from an lxml.etree._Element.
    This is used for parsing characteristcs from an XBRL instance in XML format.
    :returns EntityCharacteristic: the EntityCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    characteristic_repository: CharacteristicRepository = (
        filing_context.get_characteristic_repository()
    )

    identifier_element = error_on_none(
        xml_element.find("{*}identifier", namespaces=None),
        f"Could not find identifier element in {xml_element}",
    )

    if "scheme" not in identifier_element.attrib:
        raise ValueError("Could not find scheme attribute in identifier element")

    # The identifier element is guaranteed according to the XBRL 2.1 specification to have a text element
    entity_id_elem = error_on_none(
        xml_element.find("{*}identifier", namespaces=None),
        f"Could not find identifier element in {xml_element}",
    )
    entity_id = error_on_none(
        entity_id_elem.text,
        f"Could not find text in identifier element {entity_id_elem}",
    )

    if characteristic_repository.has(entity_id, EntityCharacteristic):
        return characteristic_repository.get(entity_id, EntityCharacteristic)
    else:
        entity_url = error_on_none(
            identifier_element.get("scheme"),
            f"Could not find scheme attribute in identifier element {identifier_element}",
        )

        entity_characteristic = EntityCharacteristic(entity_id, entity_url)
        characteristic_repository.upsert(entity_id, entity_characteristic)
        return entity_characteristic
