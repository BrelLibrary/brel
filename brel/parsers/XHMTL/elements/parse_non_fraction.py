from typing import Optional, Set
from brel.brel_context import Context
from brel.brel_fact import Fact
from brel.data.errors.error_repository import ErrorRepository
from brel.errors.error_code import ErrorCode

from brel.parsers.XHMTL.xhtml_parse_transformation_registry import (
    parse_numerical_fact_value,
)
from brel.parsers.utils.lxml_utils import (
    find_element,
    get_prefix_localname_tag,
    get_str_attribute_optional,
)
from lxml.etree import _Element
from lxml import etree
from brel.contexts.filing_context import FilingContext


def parse_decimals_or_precision(
    str_value: str | None, is_decimals: bool
) -> float | None:
    if str_value is None:
        return None

    try:
        value = float(int(str_value))
    except ValueError:
        if str_value == "INF":
            value = float("inf")
        else:
            raise ValueError(
                f"{'Decimals' if is_decimals else 'Precision'} should be an integer or 'INF'. Got {str_value} instead."
            )

    return value


def validate_descendant_non_fraction_rules(
    element: _Element, error_repository: ErrorRepository
) -> None:
    parent = element.getparent()

    if parent is None:
        return

    parent_tag = get_prefix_localname_tag(parent)
    parent_is_non_fraction = parent_tag == "ix:nonFraction"

    if not parent_is_non_fraction:
        return

    xsi_nil = get_str_attribute_optional(element, "xsi:nil")
    if xsi_nil == "true":
        error_repository.insert(
            ErrorCode.IXBRL_NIL_ATTRIBUTE_IN_NON_FRACTION_CHILD, element
        )

    parent_format = get_str_attribute_optional(parent, "format")
    parent_scale = get_str_attribute_optional(parent, "scale")
    parent_unit = get_str_attribute_optional(parent, "unitRef")

    this_format = get_str_attribute_optional(element, "format")
    this_scale = get_str_attribute_optional(element, "scale")
    this_unit = get_str_attribute_optional(element, "unitRef")

    if (
        this_format != parent_format
        or this_scale != parent_scale
        or this_unit != parent_unit
    ):
        error_repository.insert(
            ErrorCode.IXBRL_DIFFERING_FORMAT_SCALE_OR_UNIT_FOR_NON_FRACTION_CHILD,
            parent,
            this_format=this_format,
            this_scale=this_scale,
            this_unit=this_unit,
            parent_format=parent_format,
            parent_scale=parent_scale,
            parent_unit=parent_unit,
        )


def process_non_fraction_value(
    fact_element: _Element, error_repository: ErrorRepository
) -> str:
    format = get_str_attribute_optional(fact_element, "format")
    scale = get_str_attribute_optional(fact_element, "scale")
    sign = get_str_attribute_optional(fact_element, "sign")

    if sign and sign != "-":
        error_repository.insert(
            ErrorCode.IXBRL_INVALID_SIGN_ATTRIBUTE_VALUE, fact_element, sign=sign
        )

        sign = None  # Ignore sign

    fact_value = fact_element.text

    if not fact_value:
        fact_value = ""

    if not format:
        value = None
        try:
            value = float(fact_value)
        except:
            error_repository.insert(
                ErrorCode.IXBRL_NON_NUMERICAL_NON_FRACTION_FACT_VALUE,
                fact_element,
                value=fact_value,
            )

            return ""

        if value < 0:
            error_repository.insert(
                ErrorCode.IXBRL_NEGATIVE_NON_FRACTION_FACT_VALUE,
                fact_element,
                value=fact_value,
            )

            return ""

        format = "ixt:num-dot-decimal"

    if not scale:
        scale = "0"

    parsed_value = parse_numerical_fact_value(
        fact_value, format, scale, fact_element, error_repository
    )

    if sign == "-":
        parsed_value = "-" + parsed_value

    return parsed_value


def parse_non_fraction_fact_element(
    fact_element: _Element,
    context: Context,
    filing_context: FilingContext,
    taken_ids=Set[str],
) -> Fact:
    error_repository = filing_context.get_error_repository()
    id = get_str_attribute_optional(fact_element, "id")

    if id is not None and id in taken_ids:
        error_repository.insert(
            ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID, fact_element, id=id
        )

    if id is not None:
        taken_ids.add(id)

    decimals_str = get_str_attribute_optional(fact_element, "decimals")
    precision_str = get_str_attribute_optional(fact_element, "precision")

    decimals: Optional[float] = None
    try:
        decimals = parse_decimals_or_precision(decimals_str, True)
    except ValueError:
        error_repository.insert(
            ErrorCode.INVALID_DECIMALS_ATTRIBUTE_VALUE,
            fact_element,
            decimals=decimals_str,
        )

    precision: Optional[float] = None
    try:
        precision = parse_decimals_or_precision(precision_str, False)
    except ValueError:
        error_repository.insert(
            ErrorCode.INVALID_PRECISION_ATTRIBUTE_VALUE,
            fact_element,
            precision=precision_str,
        )
    xsi_nil = get_str_attribute_optional(fact_element, "xsi:nil")

    if (
        decimals != None
        and precision != None
        or precision != None
        and xsi_nil != None
        or decimals != None
        and xsi_nil != None
    ):
        error_repository.insert(
            ErrorCode.IXBRL_MUTUALLY_EXCLUSIVE_ATTRIBUTES_IN_NON_FRACTION,
            fact_element,
            id=id,
        )

    element_text = fact_element.text
    element_children = [child for child in fact_element]

    has_text = element_text != None or any([child.tail for child in element_children])
    has_children = len(element_children) > 0

    if has_text and has_children:
        error_repository.insert(
            ErrorCode.IXBRL_BOTH_TEXT_AND_CHILDREN_IN_NON_FRACTION, fact_element
        )

    if xsi_nil == "true" and (has_text or has_children):
        error_repository.insert(ErrorCode.IXBRL_TEXT_OR_CHILDREN_WITH_NIL, fact_element)

    if (not xsi_nil or xsi_nil == "false") and not has_text and not has_children:
        error_repository.insert(
            ErrorCode.IXBRL_NO_TEXT_OR_CHILDREN_WITH_ABSENT_NIL_ATTRIBUTE,
            fact_element,
        )

        # Assume xsi_nil, since fact is missing.
        xsi_nil = "true"

    validate_descendant_non_fraction_rules(fact_element, error_repository)

    fact_value = fact_element.text or ""
    if xsi_nil == "true":
        fact_value = ""
    elif has_text:
        fact_value = process_non_fraction_value(fact_element, error_repository)
    else:
        if len(element_children) > 1:
            error_repository.insert(
                ErrorCode.IXBRL_MULTIPLE_NON_FRACTION_CHILDREN, fact_element
            )

        child_tag = get_prefix_localname_tag(element_children[0])
        if child_tag != "ix:nonFraction":
            error_repository.insert(
                ErrorCode.IXBRL_INVALID_NON_FRACTION_CHILD,
                fact_element,
                child_tag=child_tag,
            )

        # Input whole element as fact value
        fact_value = etree.tostring(element_children[0]).decode()

    return Fact(context, fact_value, id, decimals, precision)
