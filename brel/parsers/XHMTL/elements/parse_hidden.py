from lxml.etree import _Element

from brel.contexts.filing_context import FilingContext
from brel.errors.error_code import ErrorCode

from brel.parsers.utils.lxml_utils import get_prefix_localname_tag


def validate_hidden_elements(
    hidden_elements: list[_Element], filing_context: FilingContext
) -> None:
    error_repository = filing_context.get_error_repository()
    for element in hidden_elements:
        for child in element:
            child_tag = get_prefix_localname_tag(child)

            if child_tag in ["ix:footnote", "ix:nonFraction", "ix:nonNumeric"]:
                continue
            elif child_tag in ["ix:fraction", "ix:tuple"]:
                error_repository.insert(
                    ErrorCode.IXBRL_ELEMENT_NOT_SUPPORTED, element, tag=child_tag
                )
            else:
                error_repository.insert(
                    ErrorCode.IXBRL_INVALID_HIDDEN_ELEMENT, element, tag=child_tag
                )
