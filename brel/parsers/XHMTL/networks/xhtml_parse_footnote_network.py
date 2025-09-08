from collections import defaultdict
import itertools
from typing import Dict, List, Optional, Set, Tuple
from brel.brel_context import Context
from lxml.etree import _Element
from lxml import etree

from brel.brel_fact import Fact
from brel.contexts.filing_context import FilingContext
from brel.data.errors.error_repository import ErrorRepository
from brel.data.fact.fact_repository import FactRepository
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
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
    footnote_element: _Element,
    continuation_chain: List[_Element],
    error_repository: ErrorRepository,
    taken_ids: Set[str],
) -> Optional[Tuple[str, BrelFootnote]]:
    id = get_str_attribute_optional(footnote_element, "id")
    if not id:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_FOOTNOTE_WITHOUT_ID, footnote_element
            )
        )
        return None

    if id in taken_ids:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, footnote_element, id=id
            )
        )

    taken_ids.add(id)

    role = get_str_attribute_optional(footnote_element, "footnoteRole")
    if role is None:
        role = "http://www.xbrl.org/2003/role/footnote"
    elif not is_valid_uri(role):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_INVALID_FOOTNOTE_ROLE,
                footnote_element,
                id=id,
                role=role,
            )
        )

        # Assuming default role
        role = "http://www.xbrl.org/2003/role/footnote"

    language = get_elem_lang_recursive(footnote_element)

    if not language:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_FOOTNOTE_WITHOUT_LANGUAGE, footnote_element, id=id
            )
        )

        # Assuming English Language
        language = "en"

    relevant_content = extract_relevant_content_from_continuation_chain(
        [footnote_element] + continuation_chain
    )
    content_text = etree.tostring(relevant_content).decode()

    title = get_str_attribute_optional(footnote_element, "title")
    return id, BrelFootnote(content_text, id, language, role, id, title)


def parse_footnotes(
    footnote_elements: List[_Element],
    continuation_chains: Dict[_Element, List[_Element]],
    error_repository: ErrorRepository,
    taken_ids: Set[str],
) -> Dict[str, BrelFootnote]:
    footnotes: Dict[str, BrelFootnote] = {}

    for footnote_element in footnote_elements:
        continuation_chain = continuation_chains.get(footnote_element) or []
        id_and_footnote = parse_footnote(
            footnote_element, continuation_chain, error_repository, taken_ids
        )

        if id_and_footnote:
            id, footnote = id_and_footnote
            footnotes[id] = footnote

    return footnotes


def parse_relationship_from_and_to_refs(
    relationship_element: _Element, error_repository: ErrorRepository
) -> Tuple[Set[str], Set[str]]:
    fromRefs = get_str_attribute_optional(relationship_element, "fromRefs")
    if not fromRefs:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_WITHOUT_FROMREFS,
                relationship_element,
            )
        )
        fromRefs = ""

    toRefs = get_str_attribute_optional(relationship_element, "toRefs")
    if not toRefs:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_WITHOUT_TOREFS,
                relationship_element,
            )
        )
        toRefs = ""

    fromIds, toIds = set(fromRefs.split()), set(toRefs.split())

    return fromIds, toIds


def validate_relationship_from_and_to_refs(
    relationship_element: _Element,
    fromIds: Set[str],
    toIds: Set[str],
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
    error_repository: ErrorRepository,
) -> None:
    # Check if any token is repeated in both fromRefs and toRefs - this is illegal
    if any([fromId in toIds for fromId in fromIds]):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_REPEATED_ID,
                relationship_element,
            )
        )

    # Check if any token in fromRefs is not a valid fact
    invalid_from_ids = [
        fromId
        for fromId in fromIds
        if fact_repository.get_by_id_optional(fromId) is None
    ]

    if invalid_from_ids:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_INVALID_FACT_ID_IN_FROMREFS,
                relationship_element,
                invalid_ids=str(invalid_from_ids),
            )
        )

    # Check if any token in toRefs is not a valid fact or footnote
    invalid_to_ids = [
        toId
        for toId in toIds
        if fact_repository.get_by_id_optional(toId) is None and toId not in footnotes
    ]
    if invalid_to_ids:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_INVALID_FACT_OR_FOOTNOTE_ID_IN_TOREFS,
                relationship_element,
                invalid_ids=str(invalid_to_ids),
            )
        )

    # Check if all tokens in toRefs are only footnotes or only facts
    are_footnotes = [toId in footnotes for toId in toIds]
    if any(are_footnotes) and not all(are_footnotes):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_MIXED_FACT_AND_FOOTNOTES_IN_TOREFS,
                relationship_element,
            )
        )


def parse_relationship_attributes(
    relationship_element: _Element, error_repository: ErrorRepository
) -> Tuple[str, str, float]:
    arcrole = get_str_attribute_optional(relationship_element, "arcrole")
    if not arcrole:
        arcrole = "http://www.xbrl.org/2003/arcrole/fact-footnote"
    elif not is_valid_uri(arcrole):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_INVALID_ARCROLE,
                relationship_element,
                arcrole=arcrole,
            )
        )

        # Assume default arcrole
        arcrole = "http://www.xbrl.org/2003/arcrole/fact-footnote"

    linkrole = get_str_attribute_optional(relationship_element, "linkRole")
    if not linkrole:
        linkrole = "http://www.xbrl.org/2003/role/link"
    elif not is_valid_uri(linkrole):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.IXBRL_RELATIONSHIP_INVALID_LINKROLE,
                relationship_element,
                linkrole=linkrole,
            )
        )
        # Assume default linkrole
        linkrole = "http://www.xbrl.org/2003/role/link"

    order_str = get_str_attribute_optional(relationship_element, "order")

    if order_str:
        try:
            order = float(order_str)
        except ValueError:
            error_repository.upsert(
                ErrorInstance.create_error_instance(
                    ErrorCode.IXBRL_RELATIONSHIP_INVALID_ORDER,
                    relationship_element,
                    order=order_str,
                )
            )

    if not order:
        order = 1.0

    return (arcrole, linkrole, order)


def parse_relationship(
    relationship_element: _Element,
    footnotes: Dict[str, BrelFootnote],
    fact_repository: FactRepository,
    error_repository: ErrorRepository,
) -> Optional[Tuple[Set[str], Set[str], str, str, float]]:
    fromIds, toIds = parse_relationship_from_and_to_refs(
        relationship_element, error_repository
    )

    validate_relationship_from_and_to_refs(
        relationship_element,
        fromIds,
        toIds,
        footnotes,
        fact_repository,
        error_repository,
    )

    arcrole, linkrole, order = parse_relationship_attributes(
        relationship_element, error_repository
    )

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
    error_repository: ErrorRepository,
) -> List[FootnoteNetwork]:
    arcs = []

    for relationship_element in relationship_elements:
        relationship = parse_relationship(
            relationship_element, footnotes, fact_repository, error_repository
        )

        if relationship:
            arcs.append(relationship)

    footnote_networks = build_footnote_networks(arcs, footnotes, fact_repository)
    return footnote_networks


def parse_role_reference(
    role_ref_element: _Element, error_repository: ErrorRepository
) -> None:
    link_type = get_str_attribute_optional(role_ref_element, "xlink:linktype")
    if link_type != "simple":
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.ROLEREF_INVALID_LINKTYPE, role_ref_element, linktype=link_type
            )
        )
    href = get_str_attribute_optional(role_ref_element, "xlink:href")
    if not href:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.ROLEREF_MISSING_HREF_ATTRIBUTE,
                role_ref_element,
            )
        )
    elif not is_valid_uri(href):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.ROLEREF_INVALID_HREF_ATTRIBUTE, role_ref_element, href=href
            )
        )

    role_uri = get_str_attribute_optional(role_ref_element, "roleURI")
    if not role_uri:
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.ROLEREF_MISSING_ROLE_URI_ATTRIBUTE, role_ref_element
            )
        )
    elif not is_valid_uri(role_uri):
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.ROLEREF_INVALID_ROLE_URI_ATTRIBUTE,
                role_ref_element,
                role_uri=role_uri,
            )
        )

    role = get_str_attribute_optional(role_ref_element, "xlink:role")
    if role != None and role == "":
        error_repository.upsert(
            ErrorInstance.create_error_instance(
                ErrorCode.ROLEREF_EMPTY_ROLE_ATTRIBUTE, role_ref_element
            )
        )


def parse_role_references(
    role_ref_elements: List[_Element],
    arcrole_ref_elements: List[_Element],
    error_repository: ErrorRepository,
) -> None:
    for role_ref_element in role_ref_elements + arcrole_ref_elements:
        parse_role_reference(role_ref_element, error_repository)


def parse_footnote_networks_xhtml(
    context: FilingContext,
    footnote_network_elements: xhtml_footnote_network_elements.XHTMLFootnoteNetworkElements,
) -> None:
    fact_repository = context.get_fact_repository()
    error_repository = context.get_error_repository()

    parse_role_references(
        footnote_network_elements.role_ref_elements,
        footnote_network_elements.arcrole_ref_elements,
        error_repository,
    )

    footnotes = parse_footnotes(
        footnote_network_elements.footnote_elements,
        footnote_network_elements.continuation_chains,
        error_repository,
        footnote_network_elements.taken_ids,
    )

    footnote_networks = parse_relationships(
        footnote_network_elements.relationship_elements,
        footnotes,
        fact_repository,
        error_repository,
    )

    network_repository = context.get_network_repository()
    for footnote_network in footnote_networks:
        network_repository.upsert(footnote_network)
