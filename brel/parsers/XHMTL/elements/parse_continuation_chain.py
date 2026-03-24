from copy import deepcopy
from typing import Dict, Set, cast
from lxml import etree
from lxml.etree import _Element

from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode

from brel.parsers.utils.lxml_utils import (
    clone_element_without_children,
    get_prefix_localname_tag,
    get_str_attribute,
    get_str_attribute_optional,
    has_str_attribute,
)


def build_continuation_element_index(
    continuation_elements: list[_Element],
    error_repository: ErrorRepository,
    taken_ids: Set[str],
) -> Dict[str, _Element]:
    # Check that all ix:continuation elements have an id
    for continuation_element in continuation_elements:
        id = get_str_attribute_optional(continuation_element, "id")
        if id is None:
            error_repository.insert(
                ErrorCode.IXBRL_CONTINUATION_WITHOUT_ID, continuation_element
            )

            continue

        if id in taken_ids:
            error_repository.insert(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID,
                continuation_element,
                id=id,
            )

        taken_ids.add(id)

    continuation_element_index: Dict[str, _Element] = {
        get_str_attribute(continuation_element, "id"): continuation_element
        for continuation_element in continuation_elements
        if has_str_attribute(continuation_element, "id")
    }

    return continuation_element_index


def create_continuation_chains(
    fact_elements: list[_Element],
    footnote_elements: list[_Element],
    continuation_elements: list[_Element],
    error_repository: ErrorRepository,
    taken_ids: Set[str],
) -> Dict[_Element, list[_Element]]:
    continuation_element_index: Dict[str, _Element] = build_continuation_element_index(
        continuation_elements, error_repository, taken_ids
    )

    non_numeric_fact_elements: list[_Element] = list(
        filter(lambda x: "nonNumeric" in get_prefix_localname_tag(x), fact_elements)
    )

    elements_which_can_continue = non_numeric_fact_elements + footnote_elements

    used_continuation_ids: Set[str] = set()
    continuation_chains: Dict[_Element, list[_Element]] = {}
    for element in elements_which_can_continue:
        continued_at = get_str_attribute_optional(element, "continuedAt")

        continuation_chain = []
        while continued_at != None:
            if continued_at in used_continuation_ids:
                error_repository.insert(
                    ErrorCode.IXBRL_REUSED_CONTINUATION,
                    element,
                    id=continued_at,
                    element_id=get_str_attribute_optional(element, "id"),
                )

            continuation = continuation_element_index.get(continued_at)
            if continuation is None:
                error_repository.insert(
                    ErrorCode.IXBRL_INVALID_CONTINUATION_ID,
                    element,
                    id=continued_at,
                    element_id=get_str_attribute_optional(element, "id"),
                )

                break

            continuation_chain.append(continuation)
            used_continuation_ids.add(continued_at)
            continued_at = get_str_attribute_optional(continuation, "continuedAt")

        continuation_chains[element] = continuation_chain

    for footnote_or_non_numeric, continuations in continuation_chains.items():
        whole_fact_elements = [footnote_or_non_numeric] + continuations
        for element in whole_fact_elements:
            for descendant in element.iterdescendants("{*}continuation", element.tag):
                if descendant in whole_fact_elements:
                    error_repository.insert(
                        ErrorCode.IXBRL_INVALID_DESCENDANT_IN_CONTINUATION_CHAIN,
                        descendant,
                        descendant_id=get_str_attribute_optional(descendant, "id"),
                        parent_id=get_str_attribute_optional(element, "id"),
                    )

    unused_continuation_elements = list(
        set(continuation_element_index.keys()) - used_continuation_ids
    )
    if len(unused_continuation_elements) > 0:
        error_repository.insert(
            ErrorCode.IXBRL_UNUSED_CONTINUATION_ELEMENTS,
            continuation_element_index.get(unused_continuation_elements[0]),
            element_ids=str(unused_continuation_elements),
        )

    return continuation_chains


def append_text_to_parent(parent: _Element, text: str | None) -> None:
    if text is None:
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
    relevant_element = clone_element_without_children(element)

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
    merged_element = clone_element_without_children(elements[0])
    merged_element.text = None

    for element in elements:
        append_text_to_parent(merged_element, element.text)

        for child in element:
            merged_element.append(child)

    return merged_element


def extract_relevant_content_from_continuation_chain(
    continuation_chain: list[_Element],
) -> _Element:
    relevant_content = [
        extract_relevant_content_per_element(element) for element in continuation_chain
    ]

    return merge_relevant_content(relevant_content)
