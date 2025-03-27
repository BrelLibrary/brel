"""
This module contains the function to parse a PeriodCharacteristic from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.1
- date: 20 December 2023

====================
"""

from typing import Callable, cast

import lxml.etree

from brel.characteristics import Aspect, ICharacteristic, PeriodCharacteristic


def parse_period_from_xml(
    xml_element: lxml.etree._Element,
    get_from_cache: Callable[[str], ICharacteristic | Aspect | None],
    add_to_cache: Callable[[str, ICharacteristic | Aspect], None],
) -> PeriodCharacteristic:
    """
    Create a Period from an lxml.etree._Element.
    :param xml_element: the lxml.etree._Element from which the PeriodCharacteristic is created
    :param make_qname: the function to make a QName from a string
    :param get_from_cache: the function to get a characteristic from the characteristics cache
    :param add_to_cache: the function to add a characteristic to the characteristics cache
    :returns: the PeriodCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """

    is_instant = xml_element.find("{*}instant", namespaces=None) is not None
    if is_instant:
        instant_date_elem = xml_element.find("{*}instant", namespaces=None)
        if instant_date_elem is None:
            raise ValueError("Could not find instant element in period characteristic")
        instant_date = instant_date_elem.text
        if instant_date is None:
            raise ValueError("The instant element has no text")

        # check cache
        period_characteristic = get_from_cache(f"period {instant_date}")
        if period_characteristic is not None:
            # if the period characteristic is already in the cache, typecheck it and return it
            if not isinstance(period_characteristic, PeriodCharacteristic):
                raise ValueError("Period characteristic is not a period characteristic")
            return cast(PeriodCharacteristic, period_characteristic)
        else:
            # if the period characteristic is not in the cache, create it and add it to the cache
            period_characteristic = PeriodCharacteristic._instant(instant_date)
            add_to_cache(f"period {instant_date}", period_characteristic)
            return period_characteristic

    else:
        start_date_elem = xml_element.find("{*}startDate", namespaces=None)
        if start_date_elem is None:
            raise ValueError("Could not find startDate element in period characteristic")
        start_date = start_date_elem.text
        if start_date is None:
            raise ValueError("The startDate element has no text")

        end_date_elem = xml_element.find("{*}endDate", namespaces=None)
        if end_date_elem is None:
            raise ValueError("Could not find endDate element in period characteristic")
        end_date = end_date_elem.text
        if end_date is None:
            raise ValueError("The endDate element has no text")

        # check cache
        period_characteristic = get_from_cache(f"period {start_date} {end_date}")
        if period_characteristic is not None:
            # if the period characteristic is already in the cache, typecheck it and return it
            if not isinstance(period_characteristic, PeriodCharacteristic):
                raise ValueError("Period characteristic is not a period characteristic")
            return cast(PeriodCharacteristic, period_characteristic)
        else:
            # if the period characteristic is not in the cache, create it and add it to the cache
            period_characteristic = PeriodCharacteristic._duration(start_date, end_date)
            add_to_cache(f"period {start_date} {end_date}", period_characteristic)
            return period_characteristic
