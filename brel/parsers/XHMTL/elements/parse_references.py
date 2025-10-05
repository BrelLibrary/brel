from typing import Set
from lxml.etree import _Element

from brel.contexts.filing_context import FilingContext
from brel.errors.error_code import ErrorCode

from brel.parsers.utils.lxml_utils import (
    get_prefix_localname_tag,
    get_str_attribute_optional,
)


def parse_references_elements(
    elements: list[_Element], taken_ids: Set[str], filing_context: FilingContext
) -> None:
    error_repository = filing_context.get_error_repository()

    for element in elements:
        id = get_str_attribute_optional(element, "id")
        if id is not None:
            if id in taken_ids:
                error_repository.insert(
                    ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, element, id=id
                )

            taken_ids.add(id)

        if len(element) == 0:
            error_repository.insert(
                ErrorCode.IXBRL_REFERENCES_ELEMENT_WITHOUT_CHILDREN, element
            )

        for child in element:
            child_tag = get_prefix_localname_tag(child)

            if child_tag not in ["link:schemaRef", "link:linkbaseRef"]:
                error_repository.insert(
                    ErrorCode.IXBRL_INVALID_REFERENCES_CHILD, child, child_tag=child_tag
                )
