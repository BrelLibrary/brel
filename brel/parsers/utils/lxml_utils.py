import lxml
import lxml.etree
from typing import cast


def compute_connected_components(
    edges: list[tuple[str, str]]
) -> list[list[str]]:
    """
    Given a list of edges, compute the connected components.
    @param edges: The edges. These are tuples of the form (node1, node2).
    @return: A list of connected components. Each connected component is a list of nodes.
    """
    unvisited: set[str] = set()
    for edge in edges:
        unvisited.add(edge[0])
        unvisited.add(edge[1])

    connected_components: list[list[str]] = []
    while len(unvisited) > 0:
        # pick a random element from unvisited
        current_node = unvisited.pop()
        # create a new connected component
        connected_component: list[str] = []
        working_set: list[str] = [current_node]
        while len(working_set) > 0:
            current_node = working_set.pop()
            connected_component.append(current_node)
            for edge in edges:
                if edge[0] == current_node and edge[1] in unvisited:
                    working_set.append(edge[1])
                    unvisited.remove(edge[1])
                elif edge[1] == current_node and edge[0] in unvisited:
                    working_set.append(edge[0])
                    unvisited.remove(edge[0])

        connected_components.append(connected_component)

    return connected_components


def get_str(
    element: lxml.etree._Element, attribute: str, default: str | None = None
) -> str:
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

        raise ValueError(
            f"{attribute} attribute not found on element {element}"
        )
    if not isinstance(value, str):
        raise TypeError(
            f"{attribute} attribute on element {element} is not a string"
        )
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
