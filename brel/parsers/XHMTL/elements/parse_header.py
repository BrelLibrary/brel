from typing import List, Tuple
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode

from brel.parsers.utils.lxml_utils import (
    find_element,
    find_elements,
    get_prefix_localname_tag,
)
from lxml.etree import _Element


def check_no_header_element_in_head(
    etree: _Element, error_repository: ErrorRepository
) -> None:
    head_elements = find_elements(etree, ".//head")
    for head_element in head_elements:
        if find_element(head_element, ".//ix:header"):
            error_repository.insert(
                ErrorCode.IXBRL_HEADER_ELEMENT_IN_HEAD, head_element
            )


def parse_header(
    header_element: _Element, error_repository: ErrorRepository
) -> Tuple[List[_Element], List[_Element], List[_Element]]:
    hidden_elements, resources_elements, references_elements = [], [], []

    for child in header_element:
        tag = get_prefix_localname_tag(child)
        if tag == "ix:hidden":
            hidden_elements.append(child)
        elif tag == "ix:resources":
            resources_elements.append(child)
        elif tag == "ix:references":
            references_elements.append(child)
        else:
            error_repository.insert(
                ErrorCode.IXBRL_INVALID_HEADER_CHILD,
                header_element,
                child_tag=tag,
            )

    if len(hidden_elements) > 1:
        error_repository.insert(
            ErrorCode.IXBRL_MORE_THAN_ONE_HIDDEN_HEADER_CHILD,
            header_element,
            count=str(len(hidden_elements)),
        )

    if len(resources_elements) > 1:
        error_repository.insert(
            ErrorCode.IXBRL_MORE_THAN_ONE_RESOURCES_HEADER_CHILD,
            header_element,
            count=str(len(resources_elements)),
        )

    return hidden_elements, resources_elements, references_elements
