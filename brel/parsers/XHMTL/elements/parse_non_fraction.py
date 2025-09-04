from typing import Set
from brel.brel_context import Context
from brel.brel_fact import Fact
from brel.parsers.XHMTL.xhtml_parse_transformation_registry import (
    parse_numerical_fact_value,
)
from brel.parsers.utils.lxml_utils import (
    get_prefix_localname_tag,
    get_str_attribute_optional,
)
from lxml.etree import _Element
from lxml import etree
from brel.contexts.filing_context import FilingContext


def parse_decimals_or_precision(
    str_value: str | None, is_decimals: bool
) -> float | None:
    if str_value != None:
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

    return None


def validate_descendant_non_fraction_rules(element: _Element) -> None:
    parent = element.getparent()

    if parent is None:
        return

    parent_tag = get_prefix_localname_tag(parent)
    parent_is_non_fraction = parent_tag == "ix:nonFraction"

    if not parent_is_non_fraction:
        return

    xsi_nil = get_str_attribute_optional(element, "xsi:nil")
    if xsi_nil:
        raise ValueError(
            f"Non-fraction fact cannot have xsi:nil attribute if it is a child of another non-fraction fact."
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
        raise ValueError(
            f"Non-fraction fact cannot have different format, scale or unitRef attributes if it is a child of another non-fraction fact."
        )


def process_non_fraction_value(
    fact_value: str, format: str | None, scale: str | None, sign: str | None
) -> str:
    if not format:
        value = None
        try:
            value = float(fact_value)
        except:
            raise ValueError(f"Non-fraction fact value {fact_value} is not a number")

        if value < 0:
            raise ValueError(f"Fact value cannot be negative: {fact_value}")

        format = "ixt:num-dot-decimal"

    if not scale:
        scale = "0"

    parsed_value = parse_numerical_fact_value(fact_value, format, scale)

    if sign == "-":
        parsed_value = "-" + parsed_value

    return parsed_value


def parse_non_fraction_fact_element(
    fact_element: _Element, context: Context, taken_ids=Set[str]
) -> Fact:
    id = get_str_attribute_optional(fact_element, "id")

    if id is not None and id in taken_ids:
        raise ValueError(f"ID '{id}' has already been used.")

    if id is not None:
        taken_ids.add(id)

    decimals_str = get_str_attribute_optional(fact_element, "decimals")
    precision_str = get_str_attribute_optional(fact_element, "precision")

    decimals = parse_decimals_or_precision(decimals_str, True)
    precision = parse_decimals_or_precision(precision_str, False)

    xsi_nil = get_str_attribute_optional(fact_element, "xsi:nil")

    if (
        decimals != None
        and precision != None
        or precision != None
        and xsi_nil != None
        or decimals != None
        and xsi_nil != None
    ):
        raise ValueError(
            "Fact cannot have more than one of: decimals, precision and xsi_nil attribute. Got more than one."
        )

    if xsi_nil and xsi_nil != "true":
        raise ValueError(
            f"If xsi_nil is set, it should always be set to 'true'. Got {xsi_nil} instead."
        )

    element_text = fact_element.text
    element_children = [child for child in fact_element]

    has_text = element_text != None or any([child.tail for child in element_children])
    has_children = len(element_children) > 0

    if has_text and has_children:
        raise ValueError(f"Non-fraction fact cannot have both text and children.")

    if xsi_nil == "true" and (has_text or has_children):
        raise ValueError(
            f"Non-fraction fact cannot have text or children if the xsi:nil attribute is set to 'true'."
        )

    if not xsi_nil and not has_text and not has_children:
        raise ValueError(
            f"Non-fraction fact cannot have neither text nor children if the xsi:nil attribute is not set to 'true'."
        )

    validate_descendant_non_fraction_rules(fact_element)

    format = get_str_attribute_optional(fact_element, "format")
    scale = get_str_attribute_optional(fact_element, "scale")
    sign = get_str_attribute_optional(fact_element, "sign")

    if sign and sign != "-":
        raise ValueError(
            f"If sign is set, it should always be set to '-'. Got {sign} instead."
        )

    fact_value = fact_element.text or ""
    if xsi_nil == "true":
        fact_value = ""
    elif has_text:
        fact_value = process_non_fraction_value(fact_value, format, scale, sign)
    else:
        if len(element_children) > 1:
            raise ValueError(
                "Non-fraction fact cannot have more than one child element if it has no text."
            )

        child_tag = get_prefix_localname_tag(element_children[0])
        if child_tag != "ix:nonFraction":
            raise ValueError(
                f"Non-fraction fact cannot have a child element that is not ix:nonFraction. Got {child_tag} instead."
            )

        # Input whole element as fact value
        fact_value = etree.tostring(element_children[0]).decode()

    return Fact(context, fact_value, id, decimals, precision)
