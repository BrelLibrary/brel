from collections import defaultdict
import itertools
from typing import Dict, List, Set, Tuple
from brel.brel_context import Context
from lxml.etree import _Element
from lxml import etree

from brel.brel_fact import Fact
from brel.contexts.filing_context import FilingContext
from brel.data.fact.fact_repository import FactRepository
from brel.networks.footnote_network import FootnoteNetwork
from brel.networks.footnote_network_node import FootnoteNetworkNode
from brel.parsers.XHMTL.elements.parse_continuation_chain import (
    extract_relevant_content_from_continuation_chain,
)
from brel.parsers.XHMTL.networks import xhtml_footnote_network_elements
from brel.parsers.utils.lxml_utils import (
    get_elem_lang_recursive,
    get_str_attribute,
    get_str_attribute_optional,
)
from brel.parsers.utils.url_utils import is_valid_uri
import brel.qnames.qname as qname
from brel.qnames.qname_utils import qname_from_str
from brel.resource.brel_footnote import BrelFootnote


def parse_footnote(
    footnote_element: _Element, continuation_chain: List[_Element], taken_ids: Set[str]
) -> Tuple[str, BrelFootnote]:
    id = get_str_attribute_optional(footnote_element, "id")
    if not id:
        raise ValueError("All ix:footnote elements must have an id attribute.")
    if id in taken_ids:
        raise ValueError(f"ID '{id}' has already been used.")
    taken_ids.add(id)

    role = get_str_attribute_optional(footnote_element, "footnoteRole")
    if role is None:
        role = "http://www.xbrl.org/2003/role/footnote"
    elif not is_valid_uri(role):
        raise ValueError(
            f"Footnote with id '{id}' must have a valid URI for its footnoteRole. Got '{role}'."
        )

    language = get_elem_lang_recursive(footnote_element)
    if not language:
        raise ValueError(f"Footnote with id '{id}' does not have a language in scope.")

    relevant_content = extract_relevant_content_from_continuation_chain(
        footnote_element, continuation_chain
    )
    content_text = etree.tostring(relevant_content).decode()

    title = get_str_attribute_optional(footnote_element, "title")
    return id, BrelFootnote(content_text, id, language, role, id, title)


def parse_footnotes(
    footnote_elements: List[_Element],
    continuation_chains: Dict[_Element, List[_Element]],
    taken_ids: Set[str],
) -> Dict[str, BrelFootnote]:
    footnotes: Dict[str, BrelFootnote] = {}

    for footnote_element in footnote_elements:
        continuation_chain = continuation_chains.get(footnote_element) or []
        id, footnote = parse_footnote(footnote_element, continuation_chain, taken_ids)
        footnotes[id] = footnote

    return footnotes


def parse_relationship(
    relationship_element: _Element,
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
    taken_ids: Set[str],
) -> Tuple[Set[str], Set[str], str, str, float]:
    fromRefs = get_str_attribute_optional(relationship_element, "fromRefs")
    if not fromRefs:
        raise ValueError("All ix:relationship elements must have a fromRef attribute.")

    toRefs = get_str_attribute_optional(relationship_element, "toRefs")
    if not toRefs:
        raise ValueError("All ix:relationship elements must have a toRef attribute.")

    fromIds, toIds = set(fromRefs.split()), set(toRefs.split())

    # Check if any token is repeated in both fromRefs and toRefs - this is illegal
    if any([fromId in toIds for fromId in fromIds]):
        raise ValueError("A token in fromRefs is repeated in toRefs.")

    # Check if any token in fromRefs is not a valid fact
    if any([fact_repository.get_by_id_optional(fromId) is None for fromId in fromIds]):
        raise ValueError("All tokens in fromRefs should be valid facts.")

    # Check if any token in toRefs is not a valid fact or footnote
    if any(
        [
            fact_repository.get_by_id_optional(toId) is None and toId not in footnotes
            for toId in toIds
        ]
    ):
        raise ValueError("All tokens in toRefs should be valid facts or footnotes.")

    # Check if all tokens in toRefs are only footnotes or only facts
    if any([toId in footnotes for toId in toIds]) and not all(
        [toId in footnotes for toId in toIds]
    ):
        raise ValueError(
            "Only footnotes or only facts should be referenced in toRefs. A mix of both was found."
        )

    arcrole = get_str_attribute_optional(relationship_element, "arcrole")
    if not arcrole:
        arcrole = "http://www.xbrl.org/2003/arcrole/fact-footnote"
    elif not is_valid_uri(arcrole):
        raise ValueError(
            f"Relationship with fromRefs '{fromRefs}' and toRefs '{toRefs}' must have a valid URI for its arcrole. Got '{arcrole}'."
        )

    linkrole = get_str_attribute_optional(relationship_element, "linkRole")
    if not linkrole:
        linkrole = "http://www.xbrl.org/2003/role/link"
    elif not is_valid_uri(linkrole):
        raise ValueError(
            f"Relationship with fromRefs '{fromRefs}' and toRefs '{toRefs}' must have a valid URI for its linkRole. Got '{linkrole}'."
        )

    order_str = get_str_attribute_optional(relationship_element, "order")

    if order_str:
        try:
            order = float(order_str)
        except ValueError:
            raise ValueError(
                f"Relationship with fromRefs '{fromRefs}' and toRefs '{toRefs}' must have a valid floating-point value for its order. Got '{order}'."
            )
    else:
        order = 1.0

    return (fromIds, toIds, arcrole, linkrole, order)


def create_footnote_network_nodes(
    arcs: List[Tuple[Set[str], Set[str], str, str, float]],
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
):
    all_ids = set()
    internal_ids = set()

    # Compute Ids of root nodes
    for from_ids, to_ids, _, _, _ in arcs:
        all_ids.update(from_ids)
        all_ids.update(to_ids)
        internal_ids.update(to_ids)

    root_ids = all_ids - internal_ids

    id_to_node: Dict[str, FootnoteNetworkNode] = {}

    for from_ids, to_ids, arcrole, linkrole, order in arcs:
        for from_id in from_ids:
            if from_id not in id_to_node and from_id in root_ids:
                from_object = fact_repository.get_by_id(from_id)
                id_to_node[from_id] = FootnoteNetworkNode(
                    from_object,
                    [],
                    arcrole,
                    qname.FOOTNOTE_NETWORK_ARCNAME,
                    linkrole,
                    qname.FOOTNOTE_NETWORK_LINKNAME,
                )

        for to_id in to_ids:
            if to_id not in id_to_node:
                to_object = (
                    footnotes[to_id]
                    if to_id in footnotes
                    else fact_repository.get_by_id(to_id)
                )
                id_to_node[to_id] = FootnoteNetworkNode(
                    to_object,
                    [],
                    arcrole,
                    qname.FOOTNOTE_NETWORK_ARCNAME,
                    linkrole,
                    qname.FOOTNOTE_NETWORK_LINKNAME,
                    order,
                )

    root_nodes = [id_to_node[id] for id in root_ids]

    return id_to_node, root_nodes


def connect_footnote_network_nodes(
    arcs: List[Tuple[Set[str], Set[str], str, str, float]],
    id_to_node: Dict[str, FootnoteNetworkNode],
):
    for from_ids, to_ids, _, _, _ in arcs:
        for from_id, to_id in itertools.product(from_ids, to_ids):
            from_node = id_to_node[from_id]
            to_node = id_to_node[to_id]
            from_node._add_child(to_node)


def build_footnote_network(
    arcs: List[Tuple[Set[str], Set[str], str, str, float]],
    linkrole: str,
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
) -> FootnoteNetwork:
    id_to_node, root_nodes = create_footnote_network_nodes(
        arcs, footnotes, fact_repository
    )
    connect_footnote_network_nodes(arcs, id_to_node)

    return FootnoteNetwork(root_nodes, linkrole, qname.FOOTNOTE_NETWORK_LINKNAME, True)


def build_footnote_networks(
    arcs: List[Tuple[Set[str], Set[str], str, str, float]],
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
) -> List[FootnoteNetwork]:
    network_arcs: Dict[
        Tuple[str, str], List[Tuple[Set[str], Set[str], str, str, float]]
    ] = defaultdict(list)

    # Group arcs by linkrole and arcrole
    for arc in arcs:
        arcrole, linkrole = arc[2], arc[3]
        network_arcs[linkrole, arcrole].append(arc)

    networks: List[FootnoteNetwork] = []
    for (_, linkrole), arcs in network_arcs.items():
        network = build_footnote_network(arcs, linkrole, footnotes, fact_repository)
        networks.append(network)

    return networks


def parse_relationships(
    relationship_elements: List[_Element],
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
    taken_ids: Set[str],
) -> List[FootnoteNetwork]:
    arcs = []

    for relationship_element in relationship_elements:
        arcs.append(
            parse_relationship(
                relationship_element, footnotes, fact_repository, taken_ids
            )
        )

    footnote_networks = build_footnote_networks(arcs, footnotes, fact_repository)
    return footnote_networks


def parse_role_reference(role_ref_element: _Element) -> None:
    link_type = get_str_attribute_optional(role_ref_element, "xlink:linktype")
    if link_type != "simple":
        raise ValueError(
            f"All (arc)role references must have linktype 'simple'. Got '{link_type}'."
        )

    href = get_str_attribute_optional(role_ref_element, "xlink:href")
    if not href:
        raise ValueError("All (arc)role references must have an href attribute.")
    elif not is_valid_uri(href):
        raise ValueError(f"xlink:href can only take valid URI values. Got '{href}'.")

    role_uri = get_str_attribute_optional(role_ref_element, "roleURI")
    if not role_uri:
        raise ValueError("All (arc)role references must have a roleURI attribute.")
    elif not is_valid_uri(role_uri):
        raise ValueError(f"roleURI can only take valid URI values. Got '{role_uri}'.")

    role = get_str_attribute_optional(role_ref_element, "xlink:role")
    if role != None and role == "":
        raise ValueError(
            "If the xlink:role attribute is present in an (arc)role reference, it must not be empty."
        )


def parse_role_references(
    role_ref_elements: List[_Element], arcrole_ref_elements: List[_Element]
) -> None:
    for role_ref_element in role_ref_elements + arcrole_ref_elements:
        parse_role_reference(role_ref_element)


def parse_footnote_networks_xhtml(
    context: FilingContext,
    footnote_network_elements: xhtml_footnote_network_elements.XHTMLFootnoteNetworkElements,
) -> None:
    fact_repository = context.get_fact_repository()
    parse_role_references(
        footnote_network_elements.role_ref_elements,
        footnote_network_elements.arcrole_ref_elements,
    )
    footnotes = parse_footnotes(
        footnote_network_elements.footnote_elements,
        footnote_network_elements.continuation_chains,
        footnote_network_elements.taken_ids,
    )

    footnote_networks = parse_relationships(
        footnote_network_elements.relationship_elements,
        footnotes,
        fact_repository,
        footnote_network_elements.taken_ids,
    )

    network_repository = context.get_network_repository()
    for footnote_network in footnote_networks:
        network_repository.upsert(footnote_network)
