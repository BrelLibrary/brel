from typing import cast, Mapping

import lxml
import lxml.etree


def get_clark(prefix: str, local_name: str, prefix_to_url: Mapping[str, str]) -> str:
    """
    Given a prefix, a local name and a prefix to URL mapping, return the clark notation.
    :param prefix: The prefix.
    :param local_name: The local name.
    :param prefix_to_url: The prefix to URL mapping.
    :returns: The clark notation.
    """
    url = prefix_to_url[prefix]
    return f"{{{url}}}{local_name}"


def get_str_attribute(element: lxml.etree._Element, attribute: str, default: str | None = None) -> str:  # type: ignore
    """
    Helper function for getting a string attribute from an element. Always returns a string.
    :param element: lxml.etree._Element to get the attribute from
    :param attribute: str containing the name of the attribute
    :param default: str containing the default value to return if the attribute is not found
    :return: str containing the value of the attribute
    :raises: if the attribute is not found and no default value is provided
    :raises: if the attribute is not a string
    """
    value = element.attrib.get(attribute)
    if value is None:
        if default is not None:
            return default

        raise ValueError(f"{attribute} attribute not found on element {element}")
    return value


def get_str_tag(element: lxml.etree._Element) -> str:  # type: ignore
    """
    Helper function for getting the tag of an element as a string.
    :param element: lxml.etree._Element to get the tag from
    :returns: str containing the tag of the element
    """
    return element.tag


def get_all_nsmaps(
    lxml_etrees: list[lxml.etree._ElementTree],  # type: ignore
) -> list[dict[str, str]]:
    """
    Given a list of lxml etree objects, get all the namespace mappings.
    :param lxml_etrees: A list of lxml etree objects.
    :returns: A list of namespace mappings.
    """
    # TODO fix typing issues
    nsmaps: list[dict[str, str]] = []
    for lxml_etree in lxml_etrees:
        for xml_element in lxml_etree.iter():
            nsmap: dict[str | None, str] = xml_element.nsmap
            nsmap.update(
                {
                    str(key.replace("xmlns:", "")): str(value)  # type: ignore
                    for key, value in xml_element.attrib.items()
                    if key.startswith("xmlns:")  # type: ignore
                }
            )

            nsmap.pop(None, None)

            nsmap_typecasted = cast(dict[str, str], nsmap)
            nsmaps.append(nsmap_typecasted)

    return nsmaps
