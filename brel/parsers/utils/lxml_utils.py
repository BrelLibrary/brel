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
    :param lxml_etrees: A list of lxml etree objects.
    :returns: A list of namespace mappings.
    """
    nsmaps: list[dict[str, str]] = []
    for lxml_etree in lxml_etrees:
        for xml_element in lxml_etree.iter():
            nsmap = xml_element.nsmap
            nsmap.update(
                {key.replace("xmlns:", ""): value for key, value in xml_element.attrib.items() if key.startswith("xmlns:")}
            )

            nsmap.pop(None, None)

            nsmap_typecasted = cast(dict[str, str], nsmap)
            nsmaps.append(nsmap_typecasted)

    return nsmaps

def list_by_local_name(

    lxml_etree: lxml.etree._ElementTree,
    local_name: str,
    direct_children_only: bool = False,
    default: lxml.etree._Element | None = None,
) -> list[lxml.etree._Element]:
    """
    Given an lxml etree object and a local name, return the first element with that local name."
    
    :param lxml_etree: The lxml etree object to search within.
    :param local_name: The local name of the elements to find.
    :param direct_children_only: If True, only search direct children. Defaults to False.
    :param default: The default value to return if no elements are found. Defaults to None.
    :returns: A list of lxml elements with the specified local name.
    :raises ValueError: If no elements are found and no default is provided.
    """
    if direct_children_only:
        xpath_expression = f"./*[tag-like('{local_name}')]"
    else:
        xpath_expression = f".//*[tag-like('{local_name}')]"
    
    elements = lxml_etree.xpath(xpath_expression)
    if not elements:
        if default is not None:
            return default

        raise ValueError(f"Could not find element with local name {local_name}")
    return elements

def get_by_local_name(
    lxml_etree: lxml.etree._ElementTree,
    local_name: str,
    direct_children_only: bool = False,
    default: lxml.etree._Element | None = None,
) -> lxml.etree._Element:
    """
    Given an lxml etree object and a local name, return the first element with that local name."

    :param lxml_etree: The lxml etree object to search within.
    :param local_name: The local name of the elements to find.
    :param direct_children_only: If True, only search direct children. Defaults to False.
    :param default: The default value to return if no elements are found. Defaults to None.
    :returns: The first lxml element with the specified local name.
    :raises ValueError: If not exactly one element is found or no default is provided.
    """
    elements = list_by_local_name(lxml_etree, local_name, direct_children_only, default)
    if len(elements) > 1:
        raise ValueError(f"Found multiple elements with local name {local_name}")
    return elements[0]
