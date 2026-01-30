"""
This module contains the function to parse an EntityCharacteristic from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 April 2025

====================
"""


from typing import Optional
import lxml.etree

from brel.characteristics import EntityCharacteristic
from brel.contexts.filing_context import FilingContext
from brel.data.characteristic.characteristic_repository import CharacteristicRepository
from brel.errors.error_code import ErrorCode
from brel.parsers.utils.error_utils import error_on_none


def parse_entity_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,  # type: ignore
) -> Optional[EntityCharacteristic]:
    """
    Create a Entity from an lxml.etree._Element.
    This is used for parsing characteristcs from an XBRL instance in XML format.
    :returns EntityCharacteristic: the EntityCharacteristic created from the lxml.etree._Element
    """
    characteristic_repository = filing_context.get_characteristic_repository()
    error_repository = filing_context.get_error_repository()

    identifier_element = xml_element.find("{*}identifier", namespaces=None)

    if identifier_element is None:
        error_repository.insert(
            ErrorCode.ENTITY_MISSING_IDENTIFIER_ELEMENT, xml_element
        )
        return None

    entity_url = identifier_element.get("scheme")
    if entity_url is None:
        error_repository.insert(ErrorCode.ENTITY_IDENTIFIER_MISSING_SCHEME, xml_element)
        return None

    # The identifier element is guaranteed according to the XBRL 2.1 specification to have a text element

    entity_id = identifier_element.text

    if entity_id is None:
        f"Could not find text in identifier element {identifier_element}",
        return None

    if characteristic_repository.has(entity_id, EntityCharacteristic):
        return characteristic_repository.get(entity_id, EntityCharacteristic)
    else:
        entity_characteristic = EntityCharacteristic(entity_id, entity_url)
        characteristic_repository.upsert(entity_id, entity_characteristic)
        return entity_characteristic
