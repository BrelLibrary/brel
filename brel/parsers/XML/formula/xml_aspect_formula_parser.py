from typing import Optional
from brel.contexts.filing_context import FilingContext
from lxml.etree import _Element

from brel.formula.aspects.aspect_formula import AspectFormula
from brel.formula.aspects.concept_formula import ConceptFormula
from brel.formula.aspects.dimension.explicit_dimension_formula import (
    ExplicitDimensionFormula,
)
from brel.formula.aspects.entity_identifier_formula import EntityIdentifierFormula
from brel.formula.aspects.period.period_instant_formula import PeriodInstantFormula
from brel.formula.aspects.period.period_duration_formula import PeriodDurationFormula
from brel.formula.aspects.period.period_forever_formula import PeriodForeverFormula
from brel.formula.xpath_expression import XPathExpression
from brel.parsers.utils.lxml_utils import get_str_attribute_optional
from brel.qnames.qname_utils import qname_from_str
from brel.reportelements.concept import Concept

formula_prefix = lambda x: "{http://xbrl.org/2008/formula}" + x


def parse_concept_formula_element(
    element: _Element, context: FilingContext
) -> Optional[AspectFormula]:
    if len(element) == 0:
        return None

    for child in element:
        child_text = child.text or ""

        if child.tag == formula_prefix("qname"):
            qname = qname_from_str(child_text, child)
            return ConceptFormula(qname)
        elif child.tag == formula_prefix("qnameExpression"):
            return ConceptFormula(XPathExpression(child_text))

    return None


def parse_entity_identifier_formula_element(
    element: _Element, context: FilingContext
) -> Optional[AspectFormula]:
    scheme_str = get_str_attribute_optional(element, "scheme")
    value_str = get_str_attribute_optional(element, "value")

    if scheme_str is None and value_str is None:
        # xbrlfe:incompleteEntityIdentifierRule
        return None

    scheme = XPathExpression(scheme_str) if scheme_str is not None else None
    value = XPathExpression(value_str) if value_str is not None else None

    return EntityIdentifierFormula(scheme, value)


def parse_period_formula_element(
    element: _Element, context: FilingContext
) -> Optional[AspectFormula]:
    if len(element) != 1:
        # TODO: xbrlfe:incompletePeriodRule
        return None

    child = element[0]

    if child.tag == formula_prefix("forever"):
        return PeriodForeverFormula()
    elif child.tag == formula_prefix("instant"):
        value_expression_str = get_str_attribute_optional(child, "value")
        value_expression = (
            XPathExpression(value_expression_str)
            if value_expression_str is not None
            else None
        )
        return PeriodInstantFormula(value_expression)
    elif child.tag == formula_prefix("duration"):
        start_str = get_str_attribute_optional(child, "start")
        end_str = get_str_attribute_optional(child, "end")

        start_expression = XPathExpression(start_str) if start_str is not None else None
        end_expression = XPathExpression(end_str) if end_str is not None else None

        return PeriodDurationFormula(start_expression, end_expression)

    # TODO: error
    return None


def parse_explicit_dimension_formula_element(
    element: _Element, context: FilingContext
) -> Optional[AspectFormula]:
    dimension_str = get_str_attribute_optional(element, "dimension")

    if not dimension_str:
        # TODO: error
        return None

    dimension = qname_from_str(dimension_str, element)

    if len(element) != 1:
        # TODO: error
        return None

    child = element[0]

    if child.tag == formula_prefix("member"):
        if len(child) != 1:
            # TODO: error
            return None

        grandchild = child[0]

        if grandchild.tag == formula_prefix("qname"):
            member_qname = qname_from_str(grandchild.text or "", grandchild)
            return ExplicitDimensionFormula(dimension, member_qname)
        elif grandchild.tag == formula_prefix("qnameExpression"):
            member_xpath_expression = XPathExpression(grandchild.text or "")
            return ExplicitDimensionFormula(dimension, member_xpath_expression)

    elif child.tag == formula_prefix("omit"):
        return ExplicitDimensionFormula(dimension, None)

    return None


def parse_formula_aspect_element(
    rule_element: _Element, context: FilingContext
) -> Optional[AspectFormula]:
    tag = rule_element.tag

    if tag == formula_prefix("concept"):
        return parse_concept_formula_element(rule_element, context)
    elif tag == formula_prefix("period"):
        return parse_period_formula_element(rule_element, context)
    elif tag == formula_prefix("explicitDimension"):
        return parse_explicit_dimension_formula_element(rule_element, context)
    elif tag == formula_prefix("entityIdentifier"):
        return parse_entity_identifier_formula_element(rule_element, context)
    elif tag == formula_prefix("typedDimension"):
        return None
    elif tag == formula_prefix("unit"):
        return None
    return None
