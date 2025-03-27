from typing import cast, Mapping

import lxml
import lxml.etree


def get_clark(prefix: str, local_name: str, prefix_to_url: Mapping[str, str]) -> str:
    """
    Given a prefix, a local name and a prefix to URL mapping, return the clark notation.
    :param prefix: The prefix.
    :param local_name: The local name.
    :param prefix_to_url: The prefix to URL mapping.
    :returns str: The clark notation.
    """
    url = prefix_to_url[prefix]
    return f"{{{url}}}{local_name}"


def get_str(element: lxml.etree._Element, attribute: str, default: str | None = None) -> str:
    """
    Helper function for getting a string attribute from an element. Always returns a string.
    @param element: lxml.etree._Element to get the attribute from
    @param attribute: str containing the name of the attribute
    @param default: str containing the default value to return if the attribute is not found
    @return: str containing the value of the attribute
    @raises ValueError: if the attribute is not found and no default value is provided
    @raises TypeError: if the attribute is not a string
    """
    value = element.attrib.get(attribute)
    if value is None:
        if default is not None:
            return default

        raise ValueError(f"{attribute} attribute not found on element {element}")
    return value


def get_all_nsmaps(
    lxml_etrees: list[lxml.etree._ElementTree],
) -> list[dict[str, str]]:
    """
    Given a list of lxml etree objects, get all the namespace mappings.
    @param lxml_etrees: A list of lxml etree objects.
    @return: A list of namespace mappings.
    """
    nsmaps: list[dict[str, str]] = []
    for lxml_etree in lxml_etrees:
        for xml_element in lxml_etree.iter():
            nsmap = xml_element.nsmap
            # remove the None key
            nsmap.pop(None, None)

            # create a copy of the nsmap
            nsmap_typecasted = cast(dict[str, str], nsmap)
            nsmaps.append(nsmap_typecasted)

    return nsmaps
