from copy import deepcopy
from typing import Dict, Set

from lxml.etree import _Element
from lxml import etree
from brel.brel_context import Context
from brel.brel_fact import Fact
from brel.contexts.filing_context import FilingContext
from brel.errors.error_code import ErrorCode

from brel.parsers.XHMTL.elements.parse_continuation_chain import (
    extract_relevant_content_from_continuation_chain,
)
from brel.parsers.XHMTL.xhtml_parse_transformation_registry import (
    parse_non_numerical_fact_value,
)
from brel.parsers.utils.lxml_utils import get_str_attribute_optional


def convert_escaped_characters(text: str) -> str:
    snippets_to_replace = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&apos;",
    }

    for actual, escaped in snippets_to_replace.items():
        text = text.replace(actual, escaped)

    return text


def convert_escaped_characters_recursive(content: _Element) -> None:
    if content.text is not None:
        content.text = convert_escaped_characters(content.text)

    if content.tail is not None:
        content.tail = convert_escaped_characters(content.tail)

    for child in content:
        convert_escaped_characters_recursive(child)


def escape_content(content: _Element) -> str:
    convert_escaped_characters_recursive(content)

    text_nodes = []
    text_nodes.append(content.text if content.text else "")

    for child in content:
        child_str = etree.tostring(child).decode()
        text_nodes.append(child_str)

    full_text = "".join(text_nodes)
    return full_text


def extract_text_content(content: _Element) -> str:
    all_text_nodes = []
    all_text_nodes.append(content.text if content.text else "")

    for child in content:
        child_text = extract_text_content(child)
        all_text_nodes.append(child_text if child_text else "")
        all_text_nodes.append(child.tail if child.tail else "")

    return "".join(all_text_nodes)


def parse_non_numeric_fact_element(
    fact_element: _Element,
    context: Context,
    continuation_chain: list[_Element],
    filing_context: FilingContext,
    taken_ids=Set[str],
) -> Fact:
    error_repository = filing_context.get_error_repository()

    id = get_str_attribute_optional(fact_element, "id")

    if id is not None:
        if id in taken_ids:
            error_repository.insert(
                ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, fact_element, id=id
            )

        taken_ids.add(id)

    escape = get_str_attribute_optional(fact_element, "escape")

    if escape and escape not in ["true", "false"]:
        error_repository.insert(
            ErrorCode.IXBRL_INVALID_NON_NUMERIC_FACT_ESCAPE_ATTRIBUTE_VALUE,
            fact_element,
            value=escape,
        )

        # Assume escaping, since the attribute is present
        escape = "true"

    relevant_content = extract_relevant_content_from_continuation_chain(
        [fact_element] + continuation_chain
    )

    fact_value = None
    if escape == "true":
        fact_value = escape_content(relevant_content)
    else:
        fact_value = extract_text_content(relevant_content)

    format = get_str_attribute_optional(fact_element, "format")
    parsed_value = parse_non_numerical_fact_value(
        fact_value, format, fact_element, error_repository
    )

    return Fact(context, parsed_value, id)
