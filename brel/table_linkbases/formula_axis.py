from enum import Enum


class FormulaAxis(Enum):
    DESCENDANT = "descendant"
    CHILD = "child"
    SIBLING = "sibling"
    SIBLING_OR_DESCENDANT = "sibling-or-descendant"
    DESCENDANT_OR_SELF = "descendant-or-self"
    CHILD_OR_SELF = "child-or-self"
    SIBLING_OR_SELF = "sibling-or-self"
    SIBLING_OR_DESCENDANT_OR_SELF = "sibling-or-descendant-or-self"
