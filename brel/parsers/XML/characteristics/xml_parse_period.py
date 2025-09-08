"""
This module contains the function to parse a PeriodCharacteristic from an lxml.etree._Element.
It parses XBRL in the XML syntax.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 13 April 2025

====================
"""


from typing import Optional, cast
import lxml.etree

from brel.characteristics import PeriodCharacteristic
from brel.contexts.filing_context import FilingContext
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance


def get_context_date_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,
) -> Optional[str]:
    date = xml_element.text

    if not PeriodCharacteristic._is_date(date):
        filing_context.get_error_repository().upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.INVALID_CONTEXT_PERIOD_DATE, xml_element, date=date
            )
        )

        return None

    return date


def parse_instant_period_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,
) -> Optional[PeriodCharacteristic]:
    """
    Creates a Period from an lxml.etree._Element, returns it and adds it to the characteristics repository.
    :param xml_element: the lxml.etree._Element from which the PeriodCharacteristic is created
    :param make_qname: the function to make a QName from a string
    :returns: the PeriodCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    characteristic_repository = filing_context.get_characteristic_repository()
    instant_date = get_context_date_from_xml(filing_context, xml_element)
    if instant_date is None:
        return None

    if characteristic_repository.has(instant_date, PeriodCharacteristic):
        return characteristic_repository.get(instant_date, PeriodCharacteristic)
    else:
        # if the period characteristic is not in the cache, create it and add it to the cache
        period_characteristic = PeriodCharacteristic._instant(instant_date)
        # add_to_cache(f"period {instant_date}", period_characteristic)
        characteristic_repository.upsert(instant_date, period_characteristic)
        return period_characteristic


def parse_duration_period_from_xml(
    filing_context: FilingContext,
    start_date_elem: lxml.etree._Element,
    end_date_elem: lxml.etree._Element,
) -> Optional[PeriodCharacteristic]:
    """
    Creates a Period from an lxml.etree._Element, returns it and adds it to the characteristics repository.
    :param xml_element: the lxml.etree._Element from which the PeriodCharacteristic is created
    :param make_qname: the function to make a QName from a string
    :returns: the PeriodCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    characteristic_repository = filing_context.get_characteristic_repository()

    start_date = get_context_date_from_xml(filing_context, start_date_elem)
    end_date = get_context_date_from_xml(filing_context, end_date_elem)

    if start_date is None or end_date is None:
        return None

    period_id = f"period {start_date} {end_date}"
    if characteristic_repository.has(period_id, PeriodCharacteristic):
        return characteristic_repository.get(period_id, PeriodCharacteristic)
    else:
        # if the period characteristic is not in the cache, create it and add it to the cache
        try:
            period_characteristic = PeriodCharacteristic._duration(start_date, end_date)
        except ValueError:
            filing_context.get_error_repository().upsert(
                ErrorInstance.create_error_instance(
                    ErrorCode.DURATION_PERIOD_START_AFTER_END,
                    start_date_elem,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            return None

        # add_to_cache(f"period {start_date} {end_date}", period_characteristic)
        characteristic_repository.upsert(period_id, period_characteristic)
        return period_characteristic


def parse_period_from_xml(
    filing_context: FilingContext,
    xml_element: lxml.etree._Element,
) -> Optional[PeriodCharacteristic]:
    """
    Create a Period from an lxml.etree._Element, returns it and adds it to the characteristics repository.
    :param xml_element: the lxml.etree._Element from which the PeriodCharacteristic is created
    :param make_qname: the function to make a QName from a string
    :param get_from_cache: the function to get a characteristic from the characteristics cache
    :param add_to_cache: the function to add a characteristic to the characteristics cache
    :returns: the PeriodCharacteristic created from the lxml.etree._Element
    :raises ValueError: if the XML element is malformed
    """
    error_repository = filing_context.get_error_repository()

    instant_element = xml_element.find("./{*}instant")
    if instant_element is not None:
        return parse_instant_period_from_xml(filing_context, instant_element)
    else:
        start_date_elem = xml_element.find("./{*}startDate", namespaces=None)
        if start_date_elem is None:
            error_repository.upsert(
                ErrorInstance.create_error_instance(
                    ErrorCode.DURATION_PERIOD_MISSING_START_DATE, xml_element
                )
            )

            return None

        end_date_elem = xml_element.find("./{*}endDate", namespaces=None)
        if end_date_elem is None:
            error_repository.upsert(
                ErrorInstance.create_error_instance(
                    ErrorCode.DURATION_PERIOD_MISSING_END_DATE, xml_element
                )
            )

            return None

        return parse_duration_period_from_xml(
            filing_context, start_date_elem, end_date_elem
        )


if __name__ == "__main__":
    xml = "<period><endDate>2022-12-31</endDate><startDate>2023-01-01</startDate></period>"

    xml_element = lxml.etree.fromstring(xml)

    print(parse_period_from_xml(FilingContext(), xml_element))
