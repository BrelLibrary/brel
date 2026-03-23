from typing import Dict, List, Optional, Tuple, Type, TypeVar, cast

from brel.characteristics.brel_aspect import Aspect
from brel.contexts.filing_context import FilingContext
from lxml.etree import _Element, parse

from brel.formula.aspects.aspect_formula import AspectFormula
from brel.parsers.XML.formula.xml_aspect_formula_parser import (
    parse_concept_formula_element,
    parse_formula_aspect_element,
)

from brel.parsers.XML.formula.xml_filter_parser import parse_filter_element
from brel.parsers.utils.lxml_utils import get_str_attribute, get_str_attribute_optional
from brel.parsers.utils.url_utils import is_valid_uri
from brel.qnames.qname import QName
from brel.qnames.qname_utils import qname_from_str
from brel.reportelements.concept import Concept
from brel.reportelements.dimension import Dimension
from brel.table_linkbases.definition_model.definition_nodes.aspect_node import (
    AspectNode,
)
from brel.table_linkbases.definition_model.definition_nodes.concept_relationship_node import (
    ConceptRelationshipNode,
)
from brel.table_linkbases.definition_model.definition_nodes.definition_node import (
    DefinitionNode,
)
from brel.table_linkbases.definition_model.definition_nodes.dimension_relationship_node import (
    DimensionRelationshipNode,
)
from brel.table_linkbases.definition_model.definition_nodes.relationship_node import (
    RelationshipNode,
)
from brel.table_linkbases.definition_model.definition_nodes.rule_node import RuleNode
from brel.table_linkbases.definition_model.definition_nodes.rule_set import RuleSet
from brel.formula.filters.filter import Filter
from brel.table_linkbases.formula_axis import FormulaAxis
from brel.table_linkbases.parent_child_order import ParentChildOrder
from brel.table_linkbases.axis import Axis
from brel.table_linkbases.definition_model.breakdown import Breakdown
from brel.table_linkbases.definition_model.table import Table

xlink_prefix = lambda x: "{http://www.w3.org/1999/xlink}" + x
generic_prefix = lambda x: "{http://xbrl.org/2008/generic}" + x
table_prefix = lambda x: "{http://xbrl.org/2014/table}" + x
variable_prefix = lambda x: "{http://xbrl.org/2008/variable}" + x
formula_prefix = lambda x: "{http://xbrl.org/2008/formula}" + x


def find_table_linkbase_elements(context: FilingContext) -> List[_Element]:
    xml_service = context.get_xml_service()
    all_table_linkbases = []

    for etree in xml_service.get_all_etrees():
        root_element = etree.getroot()
        if not root_element.tag == "{http://xbrl.org/2003/linkbase}linkbase":
            continue

        generic_linkbases = [
            child
            for child in root_element.iterchildren()
            if child.tag == "{http://xbrl.org/2008/generic}link"
        ]

        table_linkbases = [
            child
            for child in generic_linkbases
            if len(
                [
                    grandchild
                    for grandchild in child.iterchildren()
                    if grandchild.tag == "{http://xbrl.org/2014/table}table"
                ]
            )
            > 0
        ]

        all_table_linkbases += table_linkbases

    return all_table_linkbases


def parse_parent_child_order(
    element: _Element, context: FilingContext
) -> ParentChildOrder:
    parent_child_order = get_str_attribute(element, "parentChildOrder", "")

    if parent_child_order not in ["", "parent-first", "children-first"]:
        # TODO: error
        pass

    return ParentChildOrder(parent_child_order)


def assert_is_xlink_type(element: _Element, type: str, context: FilingContext):
    resource_type = get_str_attribute_optional(element, xlink_prefix("type"))

    if resource_type != type:
        # TODO: error
        pass


def parse_label(element: _Element, context: FilingContext) -> Optional[str]:
    return get_str_attribute_optional(element, xlink_prefix("label"))


def parse_id(element: _Element, context: FilingContext) -> Optional[str]:
    return get_str_attribute_optional(element, "id")


def parse_table_element(
    table_element: _Element, linkrole: str, context: FilingContext
) -> Optional[Table]:
    parent_child_order = parse_parent_child_order(table_element, context)
    assert_is_xlink_type(table_element, "resource", context)
    id = parse_id(table_element, context)
    label = parse_label(table_element, context)

    return Table(linkrole, parent_child_order, id, label)


def parse_breakdown_element(breakdown_element: _Element, context: FilingContext):
    parent_child_order = parse_parent_child_order(breakdown_element, context)
    assert_is_xlink_type(breakdown_element, "resource", context)
    id = parse_id(breakdown_element, context)
    label = parse_label(breakdown_element, context)

    return Breakdown(parent_child_order, id, label)


def parse_rule_set_element(
    rule_set_element: _Element, context: FilingContext
) -> Optional[RuleSet]:
    tag = get_str_attribute_optional(rule_set_element, "tag")
    if not tag:
        # TODO: error
        return None

    rule_set = RuleSet(tag)
    for rule_element in rule_set_element:
        rule = parse_formula_aspect_element(rule_element, context)
        if rule:
            rule_set.add_rule(rule)

    return rule_set


def parse_rule_sets_for_rule_node_element(
    rule_node_element: _Element, context: FilingContext
) -> List[RuleSet]:
    default_rule_set: RuleSet = RuleSet()
    rule_sets: List[RuleSet] = []

    for child in rule_node_element:
        tag = child.tag
        if tag == table_prefix("ruleSet"):
            rule_set = parse_rule_set_element(child, context)
            if rule_set:
                rule_sets.append(rule_set)
        else:
            rule = parse_formula_aspect_element(child, context)
            if rule:
                default_rule_set.add_rule(rule)

    if len(default_rule_set.get_rules()) == 0:
        return rule_sets or [default_rule_set]

    rule_sets.append(default_rule_set)
    return rule_sets


def parse_rule_node_element(
    rule_node_element: _Element, context: FilingContext
) -> RuleNode:
    assert_is_xlink_type(rule_node_element, "resource", context)
    is_abstract = get_str_attribute(rule_node_element, "abstract", "false") == "true"
    is_merge = get_str_attribute(rule_node_element, "merge", "false") == "true"

    parent_child_order = parse_parent_child_order(rule_node_element, context)
    tag_selector = get_str_attribute_optional(rule_node_element, "tagSelector")

    id = parse_id(rule_node_element, context)
    label = parse_label(rule_node_element, context)

    rule_node = RuleNode(
        is_abstract, is_merge, parent_child_order, tag_selector, id, label
    )

    rule_sets = parse_rule_sets_for_rule_node_element(rule_node_element, context)

    for rule_set in rule_sets:
        rule_node.add_rule_set(rule_set, rule_set.get_tag())

    return rule_node


def parse_relationship_element(
    relationship_element: _Element,
    is_dimension_relationship: bool,
    context: FilingContext,
) -> Optional[RelationshipNode]:
    relationship_sources: List[QName | str] = []
    linkrole: str = "http://www.xbrl.org/2003/role/link"
    formula_axis: FormulaAxis = FormulaAxis.DESCENDANT_OR_SELF
    generations: int = 0
    parent_child_order = parse_parent_child_order(relationship_element, context)
    tag_selector: Optional[str] = get_str_attribute_optional(
        relationship_element, "tagSelector"
    )
    id = parse_id(relationship_element, context)
    label = parse_label(relationship_element, context)

    for child in relationship_element:
        tag = child.tag

        child_text = child.text or ""

        if tag == table_prefix("relationshipSource"):
            concept_exists = context.get_report_element_repository().has_typed_qname(
                qname_from_str(child_text, child), Concept
            )
            if (
                not concept_exists
                and tag != "{http://www.xbrl.org/2008/function/instance}root"
            ):
                # TODO: error
                return None

            relationship_sources.append(qname_from_str(child_text, child))
        elif tag == table_prefix("linkrole"):
            linkrole = child_text
        elif tag == table_prefix("formulaAxis"):
            if formula_axis not in [x.value for x in FormulaAxis]:
                # TODO: error
                return None
            if is_dimension_relationship and "sibling" in formula_axis.value:
                # TODO: error
                return None

            formula_axis = FormulaAxis(child_text)
        elif tag == table_prefix("generations"):
            try:
                generations = int(child_text)
                assert generations > 0
            except Exception:
                # TODO: error
                generations = 0

    if "descendant" not in formula_axis.value and generations > 1:
        # TODO: error
        return None

    if not is_dimension_relationship and relationship_sources == []:
        relationship_sources.append("{http://www.xbrl.org/2008/function/instance}root")
    if is_dimension_relationship:
        return DimensionRelationshipNode(
            relationship_sources,
            linkrole,
            formula_axis,
            generations,
            parent_child_order,
            tag_selector,
            id,
            label,
        )

    return ConceptRelationshipNode(
        relationship_sources,
        linkrole,
        formula_axis,
        generations,
        parent_child_order,
        tag_selector,
        id,
        label,
    )


def parse_concept_relationship_node_element(
    relationship_node_element: _Element, context: FilingContext
) -> Optional[ConceptRelationshipNode]:
    relationship_element = parse_relationship_element(
        relationship_node_element, is_dimension_relationship=False, context=context
    )

    if not relationship_element:
        return None

    concept_relationship_element = cast(ConceptRelationshipNode, relationship_element)

    arcrole: Optional[str] = None
    arcname: Optional[QName] = None
    linkname: Optional[QName] = None

    for child in relationship_node_element:
        tag = child.tag
        child_text = child.text or ""

        if tag == table_prefix("arcrole"):
            arcrole = child_text
        elif tag == table_prefix("arcname"):
            arcname = qname_from_str(child_text, child)
        elif tag == table_prefix("linkname"):
            linkname = qname_from_str(child_text, child)

    if not arcrole:
        # TODO: error
        return None

    if not arcname:
        # TODO: error
        return None

    if not linkname:
        # TODO: error
        return None

    concept_relationship_element.set_arcrole(arcrole)
    concept_relationship_element.set_arcname(arcname)
    concept_relationship_element.set_linkname(linkname)

    return concept_relationship_element


def parse_dimension_relationship_node_element(
    relationship_node_element: _Element, context: FilingContext
) -> Optional[DimensionRelationshipNode]:
    relationship_element = parse_relationship_element(
        relationship_node_element, is_dimension_relationship=True, context=context
    )

    if not relationship_element:
        return None

    definition_relationship_element = cast(
        DimensionRelationshipNode, relationship_element
    )

    dimension: Optional[Dimension] = None

    for child in relationship_node_element:
        tag = child.tag
        child_text = child.text or ""

        if tag == table_prefix("dimension"):
            dimension_qname = qname_from_str(child_text, child)
            has_dimension = context.get_report_element_repository().has_typed_qname(
                dimension_qname, Dimension
            )

            if not has_dimension:
                # TODO: error
                return None

            dimension = context.get_report_element_repository().get_typed_by_qname(
                dimension_qname, Dimension
            )

            if not dimension.is_explicit():
                # TODO: error
                return None

    if not dimension:
        # TODO: error
        return None

    definition_relationship_element.set_dimension(dimension)
    return definition_relationship_element


def parse_aspect_node_element(
    aspect_node_element: _Element, context: FilingContext
) -> Optional[AspectNode]:
    assert_is_xlink_type(aspect_node_element, "resource", context)

    label = parse_label(aspect_node_element, context)
    id = parse_id(aspect_node_element, context)
    aspect: Optional[Aspect] = None
    include_unreported_value = False

    for child in aspect_node_element:
        tag = child.tag

        if tag == table_prefix("conceptAspect"):
            aspect = Aspect.CONCEPT
        elif tag == table_prefix("entityIdentifierAspect"):
            aspect = Aspect.ENTITY
        elif tag == table_prefix("periodAspect"):
            aspect = Aspect.PERIOD
        elif tag == table_prefix("unitAspect"):
            aspect = Aspect.UNIT
        elif tag == table_prefix("dimensionAspect"):
            include_unreported_value = (
                get_str_attribute(child, "includeUnreportedValue", "false") == "true"
            )
            dimension_qname = qname_from_str(child.text or "", child)

            aspect_repository = context.get_aspect_repository()
            if not aspect_repository.has(dimension_qname.prefix_local_name_notation()):
                # TODO: error
                return None

            aspect = aspect_repository.get(dimension_qname.prefix_local_name_notation())

    if not aspect:
        # TODO: error
        return None

    return AspectNode(aspect, include_unreported_value, None, id, label)


def assert_xlink_arcrole(
    element: _Element, expected_arcrole: str, context: FilingContext
):
    actual_arcrole = get_str_attribute_optional(
        element, "{http://www.w3.org/1999/xlink}arcrole"
    )
    if not actual_arcrole:
        # TODO: error
        pass

    if actual_arcrole != expected_arcrole:
        # TODO: error
        pass


def parse_table_breakdown_arc(
    table_breakdown_arc_element: _Element,
    tables: Dict[str, Table],
    breakdowns: Dict[str, Breakdown],
    context: FilingContext,
) -> None:
    assert_is_xlink_type(table_breakdown_arc_element, "arc", context)
    assert_xlink_arcrole(
        table_breakdown_arc_element, "http://www.xbrl.org/2014/table#breakdown", context
    )
    from_label = get_str_attribute_optional(
        table_breakdown_arc_element, "{http://www.w3.org/1999/xlink}from"
    )
    to_label = get_str_attribute_optional(
        table_breakdown_arc_element, "{http://www.w3.org/1999/xlink}to"
    )

    if not from_label:
        # TODO: error
        return

    if not to_label:
        # TODO: error
        return

    axis = get_str_attribute_optional(table_breakdown_arc_element, "axis")
    if not axis:
        # TODO: error
        pass
    if axis not in ["x", "y", "z"]:
        # TODO: error
        pass

    order = get_str_attribute(table_breakdown_arc_element, "order", "1.0")

    table, breakdown = tables.get(from_label), breakdowns.get(to_label)
    if not table:
        # TODO: error
        return

    if not breakdown:
        # TODO: error
        return

    table.add_breakdown(Axis(axis), breakdown, int(order))


def parse_breakdown_tree_arc(
    breakdown_tree_arc_element: _Element,
    breakdowns: Dict[str, Breakdown],
    definition_nodes: Dict[str, DefinitionNode],
    context: FilingContext,
):
    assert_is_xlink_type(breakdown_tree_arc_element, "arc", context)
    assert_xlink_arcrole(
        breakdown_tree_arc_element,
        "http://xbrl.org/arcrole/2014/breakdown-tree",
        context,
    )
    from_label = get_str_attribute_optional(
        breakdown_tree_arc_element, "{http://www.w3.org/1999/xlink}from"
    )
    to_label = get_str_attribute_optional(
        breakdown_tree_arc_element, "{http://www.w3.org/1999/xlink}to"
    )

    if not from_label:
        # TODO: error
        return

    if not to_label:
        # TODO: error
        return

    order = get_str_attribute(breakdown_tree_arc_element, "order", "1.0")

    breakdown, definition_node = breakdowns.get(from_label), definition_nodes.get(
        to_label
    )
    if not breakdown:
        # TODO: error
        return

    if not definition_node:
        # TODO: error
        return

    definition_node.set_order(int(order))
    breakdown.add_root(definition_node, int(order))


def parse_definition_node_subtree_arc(
    definition_node_subtree_arc_element: _Element,
    definition_nodes: Dict[str, DefinitionNode],
    context: FilingContext,
):
    assert_is_xlink_type(definition_node_subtree_arc_element, "arc", context)
    assert_xlink_arcrole(
        definition_node_subtree_arc_element,
        "http://xbrl.org/arcrole/2014/definition-node-subtree",
        context,
    )
    from_label = get_str_attribute_optional(
        definition_node_subtree_arc_element, "{http://www.w3.org/1999/xlink}from"
    )
    to_label = get_str_attribute_optional(
        definition_node_subtree_arc_element, "{http://www.w3.org/1999/xlink}to"
    )

    if not from_label:
        # TODO: error
        return

    if not to_label:
        # TODO: error
        return

    order = get_str_attribute(definition_node_subtree_arc_element, "order", "1.0")

    from_node, to_node = definition_nodes.get(from_label), definition_nodes.get(
        to_label
    )
    if not from_node:
        # TODO: error
        return

    if not to_node:
        # TODO: error
        return

    if isinstance(from_node, RelationshipNode):
        # TODO: error
        return

    from_node.add_child(to_node, int(order))


def parse_table_filter_arc(
    table_filter_arc: _Element,
    tables: Dict[str, Table],
    filters: Dict[str, Filter],
    context: FilingContext,
):
    assert_is_xlink_type(table_filter_arc, "arc", context)
    assert_xlink_arcrole(
        table_filter_arc,
        "http://xbrl.org/arcrole/2014/table-filter",
        context,
    )
    from_label = get_str_attribute_optional(
        table_filter_arc, "{http://www.w3.org/1999/xlink}from"
    )
    to_label = get_str_attribute_optional(
        table_filter_arc, "{http://www.w3.org/1999/xlink}to"
    )

    if not from_label:
        # TODO: error
        return

    if not to_label:
        # TODO: error
        return

    order = get_str_attribute(table_filter_arc, "order", "1.0")

    complement = get_str_attribute(table_filter_arc, "complement", "false") == "true"
    table, filter = tables.get(from_label), filters.get(to_label)
    if not table:
        # TODO: error
        return

    if not filter:
        # TODO: error
        return

    filter.set_is_complement(complement)
    table.add_filter(filter)


def parse_aspect_node_filter_arc(
    aspect_node_filter_tree_arc_element: _Element,
    definition_nodes: Dict[str, DefinitionNode],
    filters: Dict[str, Filter],
    context: FilingContext,
):
    assert_is_xlink_type(aspect_node_filter_tree_arc_element, "arc", context)
    assert_xlink_arcrole(
        aspect_node_filter_tree_arc_element,
        "http://xbrl.org/arcrole/2014/aspect-node-filter",
        context,
    )
    from_label = get_str_attribute_optional(
        aspect_node_filter_tree_arc_element, "{http://www.w3.org/1999/xlink}from"
    )
    to_label = get_str_attribute_optional(
        aspect_node_filter_tree_arc_element, "{http://www.w3.org/1999/xlink}to"
    )

    if not from_label:
        # TODO: error
        return

    if not to_label:
        # TODO: error
        return

    complement = (
        get_str_attribute(aspect_node_filter_tree_arc_element, "complement", "false")
        == "true"
    )
    aspect_node, filter = definition_nodes.get(from_label), filters.get(to_label)
    if not aspect_node:
        # TODO: error
        return

    if not isinstance(aspect_node, AspectNode):
        # TODO: error
        return

    if not filter:
        # TODO: error
        return

    filter.set_is_complement(complement)
    aspect_node.add_filter(filter)


def parse_table_linkbase_element(
    table_linkbase_element: _Element, context: FilingContext
) -> List[Table]:
    """
    Parse a table linkbase element into a list of tables.

    Args:
        table_linkbase_element: The XML element to parse.
        context: The filing context to use.

    Returns:
        A list of tables parsed from the given XML element.
    """
    link_type = get_str_attribute_optional(table_linkbase_element, xlink_prefix("type"))
    if link_type != "extended":
        # TODO: error
        pass

    linkrole = get_str_attribute_optional(table_linkbase_element, xlink_prefix("role"))
    if not linkrole:
        # TODO: error
        linkrole = ""
        pass
    if not is_valid_uri(linkrole):
        # TODO: error
        pass

    def add_unique_to_dict[T](
        id: Optional[str], element: Optional[T], dict: Dict[str, T]
    ):
        if not element:
            return

        if not id:
            # TODO: error
            return

        if id in dict:
            # TODO: error
            pass

        dict[id] = element

    tables: Dict[str, Table] = {}
    breakdowns: Dict[str, Breakdown] = {}
    definition_nodes: Dict[str, DefinitionNode] = {}
    filters: Dict[str, Filter] = {}

    # Parse nodes
    for element in table_linkbase_element:
        tag = element.tag
        if tag == table_prefix("table"):
            table = parse_table_element(element, linkrole, context)
            if table:
                add_unique_to_dict(table.label, table, tables)
        elif tag == table_prefix("breakdown"):
            breakdown = parse_breakdown_element(element, context)
            if breakdown:
                add_unique_to_dict(breakdown.label, breakdown, breakdowns)
        elif tag == table_prefix("ruleNode"):
            rule_node = parse_rule_node_element(element, context)
            if rule_node:
                add_unique_to_dict(rule_node.label, rule_node, definition_nodes)
        elif tag == table_prefix("conceptRelationshipNode"):
            dimension_relationship_node = parse_dimension_relationship_node_element(
                element, context
            )
            if dimension_relationship_node:
                add_unique_to_dict(
                    dimension_relationship_node.label,
                    dimension_relationship_node,
                    definition_nodes,
                )
        elif tag == table_prefix("dimensionRelationshipNode"):
            dimension_relationship_node = parse_dimension_relationship_node_element(
                element, context
            )
            if dimension_relationship_node:
                add_unique_to_dict(
                    dimension_relationship_node.label,
                    dimension_relationship_node,
                    definition_nodes,
                )
            pass
        elif tag == table_prefix("aspectNode"):
            aspect_node = parse_aspect_node_element(element, context)
            if aspect_node:
                add_unique_to_dict(aspect_node.label, aspect_node, definition_nodes)
            pass
        elif tag.startswith("http://xbrl.org/2008/filter"):
            filter = parse_filter_element(element, context)
            if filter:
                add_unique_to_dict(filter.label, filter, filters)
        elif tag == variable_prefix("parameter"):
            pass

    # Parse edges
    for element in table_linkbase_element:
        tag = element.tag
        if tag == table_prefix("tableBreakdownArc"):
            parse_table_breakdown_arc(element, tables, breakdowns, context)
        elif tag == table_prefix("breakdownTreeArc"):
            parse_breakdown_tree_arc(element, breakdowns, definition_nodes, context)
        elif tag == table_prefix("definitionNodeSubtreeArc"):
            parse_definition_node_subtree_arc(element, definition_nodes, context)
        elif tag == table_prefix("aspectNodeFilterArc"):
            parse_aspect_node_filter_arc(element, definition_nodes, filters, context)
        elif tag == table_prefix("tableFilterArc"):
            parse_table_filter_arc(element, tables, filters, context)
        elif tag == table_prefix("tableParameterArc"):
            pass

    table_list = [table for _, table in tables.items()]
    for table in table_list:
        table.propagate_parent_child_order()

    return table_list


def parse_table_linkbase_from_xml(context: FilingContext) -> None:
    table_linkbase_elements = find_table_linkbase_elements(context)

    definition_tables = [
        parse_table_linkbase_element(table_linkbase_element, context)
        for table_linkbase_element in table_linkbase_elements
    ]

    table_linkbase_repository = context.get_table_linkbase_repository()

    for definition_table_set in definition_tables:
        for definition_table in definition_table_set:
            table_linkbase_repository.upsert_definition_table(definition_table)

    # Convert definition to structural table
    # Convert structural to layout table


if __name__ == "__main__":
    xml_document = parse(
        "C:/Users/cakas/Desktop/masters-thesis/Full_taxonomy_and_technical_documentation/taxonomy/www.eba.europa.eu/eu/fr/xbrl/crr/fws/pillar3/4.1/tab/k_100.00/k_100.00-rend.xml"
    )
    linkbase = xml_document.getroot()[5]
    parse_table_linkbase_element(linkbase, FilingContext())
