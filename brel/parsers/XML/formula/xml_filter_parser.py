from typing import Optional
from lxml.etree import _Element

from brel.contexts.filing_context import FilingContext
from brel.formula.filters.concept.concept_name_filter import ConceptNameFilter
from brel.formula.filters.dimension.explicit_dimension_filter import (
    ExplicitDimensionFilter,
)
from brel.formula.filters.dimension.explicit_dimension_filter_member import (
    ExplicitDimensionFilterMember,
)
from brel.formula.filters.dimension.member_axis import MemberAxis
from brel.formula.filters.dimension.typed_dimension_filter import TypedDimensionFilter
from brel.formula.filters.filter import Filter
from brel.formula.filters.period.forever_filter import ForeverFilter
from brel.formula.filters.period.period_date_time_filter import PeriodDateTimeFilter
from brel.formula.filters.period.period_date_time_filter_type import (
    PeriodDateTimeFilterType,
)
from brel.formula.filters.period.period_filter import PeriodFilter
from brel.formula.xpath_expression import XPathExpression
from brel.parsers.utils.lxml_utils import get_str_attribute_optional
from brel.qnames.qname import QName
from brel.qnames.qname_utils import qname_from_str

xlink_prefix = lambda x: "{http://www.w3.org/1999/xlink}" + x
filter_prefix = lambda postfix, x: "{http://xbrl.org/2014/filter/" + postfix + "}" + x


def assert_is_xlink_type(element: _Element, type: str, context: FilingContext):
    resource_type = get_str_attribute_optional(element, xlink_prefix("type"))

    if resource_type != type:
        # TODO: error
        pass


def parse_concept_name_filter_element(
    concept_name_filter_element: _Element, context: FilingContext
) -> Optional[ConceptNameFilter]:
    assert_is_xlink_type(concept_name_filter_element, "resource", context)
    id = get_str_attribute_optional(concept_name_filter_element, "id")
    label = get_str_attribute_optional(concept_name_filter_element, "label")

    concept_name_filter = ConceptNameFilter(label, id)

    for child in concept_name_filter_element:
        if child.tag != filter_prefix("concept", "concept"):
            # TODO: error
            return None

        if len(child) > 1:
            # TODO: error
            return None

        for grandchild in child:
            if grandchild.tag == filter_prefix("concept", "qname"):
                qname = qname_from_str(grandchild.text or "", grandchild)
                concept_name_filter.add_qname(qname)
            elif grandchild.text == filter_prefix("concept", "qnameExpression"):
                qname_expression = XPathExpression(grandchild.text or "")
                concept_name_filter.add_qname_expression(qname_expression)
            else:
                # TODO: error
                return None

    return concept_name_filter


def parse_dimension_element(
    dimension_element: _Element, context: FilingContext
) -> Optional[QName | XPathExpression]:
    if len(dimension_element) > 0:
        # TODO: error
        return None

    dimension: Optional[QName | XPathExpression] = None
    for child in dimension_element:
        if child.tag == filter_prefix("concept", "qname"):
            dimension = qname_from_str(child.text or "", child)
        elif child.text == filter_prefix("concept", "qnameExpression"):
            dimension = XPathExpression(child.text or "")

    if dimension is None:
        # TODO: error
        return None

    return dimension


def parse_member_element(
    member_element: _Element, context: FilingContext
) -> Optional[ExplicitDimensionFilterMember]:
    explicit_dimension_filter_member: Optional[ExplicitDimensionFilterMember] = None
    linkrole: Optional[str] = None
    arcrole: Optional[str] = None
    axis: Optional[MemberAxis] = MemberAxis.UNSPECIFIED

    for child in member_element:
        if child.tag == filter_prefix("dimension", "qname"):
            explicit_dimension_filter_member = ExplicitDimensionFilterMember(
                qname_from_str(child.text or "", child)
            )
        elif child.tag == filter_prefix("dimension", "qnameExpression"):
            explicit_dimension_filter_member = ExplicitDimensionFilterMember(
                XPathExpression(child.text or "")
            )
        elif child.tag == filter_prefix("dimension", "variable"):
            explicit_dimension_filter_member = ExplicitDimensionFilterMember(
                qname_from_str(child.text or "", child)
            )
        elif child.tag == filter_prefix("dimension", "linkrole"):
            linkrole = child.text or ""
        elif child.tag == filter_prefix("dimension", "arcrole"):
            arcrole = child.text or ""
        elif child.tag == filter_prefix("dimension", "axis"):
            try:
                axis = MemberAxis(child.text or "")
            except ValueError:
                # TODO: error
                return None

    if explicit_dimension_filter_member is None:
        # TODO: error
        return None

    if linkrole is not None:
        explicit_dimension_filter_member.set_linkrole(linkrole)
    if arcrole is not None:
        explicit_dimension_filter_member.set_arcrole(arcrole)
    if axis is not None:
        explicit_dimension_filter_member.set_axis(axis)

    return explicit_dimension_filter_member


def parse_explicit_dimension_filter_element(
    explicit_dimension_filter_element: _Element, context: FilingContext
) -> Optional[ExplicitDimensionFilter]:
    assert_is_xlink_type(explicit_dimension_filter_element, "resource", context)
    label = get_str_attribute_optional(explicit_dimension_filter_element, "label")
    id = get_str_attribute_optional(explicit_dimension_filter_element, "id")
    explicit_dimension_filter: Optional[ExplicitDimensionFilter] = None

    for child in explicit_dimension_filter_element:
        if child.tag == filter_prefix("dimension", "dimension"):
            if explicit_dimension_filter is not None:
                # TODO: error
                return None

            dimension = parse_dimension_element(child, context)
            if not dimension:
                # TODO: error
                return None

            explicit_dimension_filter = ExplicitDimensionFilter(dimension, label, id)
        elif child.tag == filter_prefix("dimension", "member"):
            if explicit_dimension_filter is None:
                # TODO: error
                return None

            member = parse_member_element(child, context)

            if not member:
                # TODO: error
                continue

            explicit_dimension_filter.add_allowed_member(member)

    if not explicit_dimension_filter:
        # TODO: error
        return None

    return explicit_dimension_filter


def parse_typed_dimension_filter_element(
    typed_dimension_filter_element: _Element, context: FilingContext
) -> Optional[TypedDimensionFilter]:
    assert_is_xlink_type(typed_dimension_filter_element, "resource", context)
    label = get_str_attribute_optional(typed_dimension_filter_element, "label")
    id = get_str_attribute_optional(typed_dimension_filter_element, "id")
    test_expression_str = get_str_attribute_optional(
        typed_dimension_filter_element, "test"
    )
    test_expression = (
        XPathExpression(test_expression_str)
        if test_expression_str is not None
        else None
    )

    for child in typed_dimension_filter_element:
        if child.tag == filter_prefix("dimension", "dimension"):
            dimension = parse_dimension_element(child, context)

            if not dimension:
                # TODO: error
                return None

            return TypedDimensionFilter(dimension, test_expression, label, id)

    return None


def parse_period_filter_element(
    period_filter_element: _Element, context: FilingContext
) -> Optional[PeriodFilter]:
    assert_is_xlink_type(period_filter_element, "resource", context)
    label = get_str_attribute_optional(period_filter_element, "label")
    id = get_str_attribute_optional(period_filter_element, "id")

    test_expression = get_str_attribute_optional(period_filter_element, "test")
    if test_expression is None:
        # TODO: error
        return None

    return PeriodFilter(XPathExpression(test_expression), label, id)


def parse_period_date_time_filter_element(
    period_start_filter_element: _Element,
    type: PeriodDateTimeFilterType,
    context: FilingContext,
) -> Optional[PeriodDateTimeFilter]:
    assert_is_xlink_type(period_start_filter_element, "resource", context)
    label = get_str_attribute_optional(period_start_filter_element, "label")
    id = get_str_attribute_optional(period_start_filter_element, "id")

    date_expression_str = get_str_attribute_optional(
        period_start_filter_element, "date"
    )
    time_expression_str = get_str_attribute_optional(
        period_start_filter_element, "time"
    )

    if not date_expression_str:
        # TODO: error
        return None

    date_expression = XPathExpression(date_expression_str)
    time_expression = (
        XPathExpression(time_expression_str)
        if time_expression_str is not None
        else None
    )
    return PeriodDateTimeFilter(
        date_expression,
        time_expression,
        type,
        label,
        id,
    )


def parse_forever_filter_element(
    forever_filter_element: _Element, context: FilingContext
) -> Optional[ForeverFilter]:
    assert_is_xlink_type(forever_filter_element, "resource", context)
    label = get_str_attribute_optional(forever_filter_element, "label")
    id = get_str_attribute_optional(forever_filter_element, "id")
    return ForeverFilter(label, id)


def parse_filter_element(
    filter_element: _Element, context: FilingContext
) -> Optional[Filter]:
    tag = filter_element.tag

    if tag == filter_prefix("concept", "conceptName"):
        return parse_concept_name_filter_element(filter_element, context)
    elif tag == filter_prefix("dimension", "explicitDimension"):
        return parse_explicit_dimension_filter_element(filter_element, context)
    elif tag == filter_prefix("dimension", "typedDimension"):
        return parse_typed_dimension_filter_element(filter_element, context)
    elif tag == filter_prefix("period", "period"):
        return parse_period_filter_element(filter_element, context)
    elif tag == filter_prefix("period", "periodStart"):
        return parse_period_date_time_filter_element(
            filter_element, PeriodDateTimeFilterType.START, context
        )
    elif tag == filter_prefix("period", "periodEnd"):
        return parse_period_date_time_filter_element(
            filter_element, PeriodDateTimeFilterType.END, context
        )
    elif tag == filter_prefix("period", "periodInstant"):
        return parse_period_date_time_filter_element(
            filter_element, PeriodDateTimeFilterType.INSTANT, context
        )
    elif tag == filter_prefix("period", "forever"):
        return parse_forever_filter_element(filter_element, context)
    return None
