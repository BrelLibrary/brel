import lxml
import lxml.etree
from collections import defaultdict
import validators

def prefix_key(prefix: str) -> str:
    # returns a key that can be used to sort prefixes
    # the key is the length of the prefix followed by the prefix itself
    # return f"{len(prefix)}#{prefix}"
    return len(prefix)

def url_key(url: str) -> str:
    # returns a key that can be used to sort urls
    # the key is the url itself followed by the length of the url
    return f"{url}"

def is_url_equal_without_version(url1: str, url2: str) -> bool:
    # checks if two urls are equal when removing version numbers
    # e.g. http://www.xbrl.org/2003/instance and http://www.xbrl.org/2003/instance-2003-12-31 are equal
    # idea: strip numbers and - and _ from the end of the url
    # then check if the urls are equal
    urls = [url1, url2]
    resulting_urls = []
    for url in urls:
        url.replace("-", "")
        url.replace("_", "")
        while url[-1].isdigit():
            url = url[:-1]
        resulting_urls.append(url)
    
    return resulting_urls[0] == resulting_urls[1]

def compute_connected_components(edges: list[tuple[str, str]]) -> list[list[str]]:
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

def combine_nsmaps(nsmaps: list[dict[str, str]]) -> tuple[dict[str, str], dict[str, str]]:
    edges = []
    for nsmap in nsmaps:
        for key, value in nsmap.items():
            if key is not None:
                edges.append((key, value))
    
    connected_components = compute_connected_components(edges)

    nsmap = {}
    redirects = {}
    for connected_component in connected_components:
        urls = []
        prefixes = []
        for element in connected_component:
            if validators.url(element):
                urls.append(element)
            else:
                prefixes.append(element)
            
        main_prefix = min(prefixes, key=prefix_key)
        main_url = max(urls, key=url_key)

        nsmap[main_prefix] = main_url
        for prefix in prefixes:
            if prefix != main_prefix:
                redirects[prefix] = main_prefix

    return nsmap, redirects

def get_all_nsmaps(lxml_etrees: list[lxml.etree._ElementTree]) -> list[dict[str,str]]:
    # the namespaces are normalized if each url always maps to the same prefix
    nsmaps: list[dict[str, str]] = []
    for lxml_etree in lxml_etrees:
        for xml_element in lxml_etree.iter():
            nsmap = xml_element.nsmap
            # remove the None key
            nsmap.pop(None, None)
            nsmaps.append(nsmap)
    
    return nsmaps