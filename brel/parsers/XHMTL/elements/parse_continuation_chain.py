from copy import deepcopy
from typing import Dict, Set
from lxml import etree
from lxml.etree import _Element

from brel.parsers.utils.lxml_utils import (
    get_prefix_localname_tag,
    get_str_attribute,
    get_str_attribute_optional,
)
from brel.qnames.qname_utils import qname_from_str


def build_continuation_element_index(
    continuation_elements: list[_Element], taken_ids: Set[str]
) -> Dict[str, _Element]:
    # Check that all ix:continuation elements have an id
    for continuation_element in continuation_elements:
        id = get_str_attribute_optional(continuation_element, "id")
        if id is None:
            raise ValueError("All ix:continuation elements must have an id attribute.")

        if id in taken_ids:
            raise ValueError(f"ID '{id}' has already been used.")
        taken_ids.add(id)

    continuation_element_index = {
        get_str_attribute(continuation_element, "id"): continuation_element
        for continuation_element in continuation_elements
    }

    return continuation_element_index


def create_continuation_chains(
    fact_elements: list[_Element],
    footnote_elements: list[_Element],
    continuation_elements: list[_Element],
    taken_ids: Set[str],
) -> Dict[_Element, list[_Element]]:
    continuation_element_index: Dict[str, _Element] = build_continuation_element_index(
        continuation_elements, taken_ids
    )

    non_numeric_fact_elements: list[_Element] = list(
        filter(lambda x: get_prefix_localname_tag(x) == "ix:nonNumeric", fact_elements)
    )

    elements_which_can_continue = non_numeric_fact_elements + footnote_elements

    used_continuation_ids: Set[str] = set()
    continuation_chains: Dict[_Element, list[_Element]] = {}
    for element in elements_which_can_continue:
        continued_at = get_str_attribute_optional(element, "continuedAt")

        continuation_chain = []
        while continued_at != None:
            if continued_at in used_continuation_ids:
                raise ValueError(
                    f"The ID {continued_at} in the continuation chain of the fact or footnote with id '{get_str_attribute_optional(element, 'id')}' has already been used."
                )

            continuation = continuation_element_index.get(continued_at)
            if continuation is None:
                raise ValueError(
                    f"One of the IDs in the continuation chain of the fact or footnote with id '{get_str_attribute_optional(element, 'id')}' does not exist."
                )

            continuation_chain.append(continuation)
            used_continuation_ids.add(continued_at)
            continued_at = get_str_attribute_optional(continuation, "continuedAt")

        continuation_chains[element] = continuation_chain

    for footnote_or_non_numeric, continuations in continuation_chains.items():
        whole_fact_elements = [footnote_or_non_numeric] + continuations
        for element in whole_fact_elements:
            for descendant in element.iterdescendants("{*}continuation", element.tag):
                if descendant in whole_fact_elements:
                    raise ValueError(
                        f"The continuation chain must not contain any element which is a descendant of any other element in the same continuation chain"
                    )

    if len(continuation_elements) != len(used_continuation_ids):
        raise ValueError(
            f"Found {len(continuation_elements)} ix:continuation elements but only {len(used_continuation_ids)} were used."
        )

    return continuation_chains


def append_text_to_parent(parent: _Element, text: str | None) -> None:
    if text == None:
        return

    if len(parent) == 0:
        if parent.text == None:
            parent.text = ""

        parent.text += text
    else:
        if parent[-1].tail == None:
            parent[-1].tail = ""

        parent[-1].tail += text


def extract_relevant_content_per_element(element: _Element) -> _Element:
    relevant_element = deepcopy(element)
    children = [child for child in relevant_element]

    for child in children:
        relevant_element.remove(child)

    for child in element:
        child_tag = get_prefix_localname_tag(child)

        if child_tag == "ix:exclude":
            append_text_to_parent(relevant_element, child.tail)
            continue

        relevant_child = extract_relevant_content_per_element(child)

        if child_tag.startswith("ix:"):
            append_text_to_parent(relevant_element, relevant_child.text)

            for relevant_grandchild in relevant_child:
                relevant_element.append(relevant_grandchild)

            append_text_to_parent(relevant_element, relevant_child.tail)
            continue

        relevant_element.append(relevant_child)

    return relevant_element


def merge_relevant_content(elements: list[_Element]) -> _Element:
    merged_element = etree.Element(elements[0].tag)

    for element in elements:
        append_text_to_parent(merged_element, element.text)

        for child in element:
            merged_element.append(child)

    return merged_element


def extract_relevant_content_from_continuation_chain(
    fact_element: _Element, continuation_chain: list[_Element]
) -> _Element:
    head_content = extract_relevant_content_per_element(fact_element)
    tail_content = [
        extract_relevant_content_per_element(element) for element in continuation_chain
    ]

    return merge_relevant_content([head_content] + tail_content)
