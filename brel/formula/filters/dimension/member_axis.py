from enum import Enum


class MemberAxis(Enum):
    CHILD = "child"
    CHILD_OR_SELF = "child-or-self"
    DESCENDANT = "descendant"
    DESCENDANT_OR_SELF = "descendant-or-self"
    UNSPECIFIED = ""
