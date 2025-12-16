from enum import Enum


class ParentChildOrder(Enum):
    PARENT_FIRST = "parent-first"
    CHILDREN_FIRST = "children-first"
    UNSPECIFIED = ""
