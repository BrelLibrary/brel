

from typing import Any, Dict, Optional, Union

from brel.errors.area import Area
from brel.errors.error_code import ErrorCode
from brel.errors.severity import Severity


error_registry: Dict[ErrorCode, Dict[str, Union[Severity, Area, str]]] = {
    ErrorCode.MISSING_CONTEXT_PERIOD: {
        "severity": Severity.ERROR,
        "area": Area.GENERAL_INSTANCE,
        "numeric_code": "000",
        "message": "Context is missing a period child element",
        "hint": "Check the definition of the context."
    },

    ErrorCode.MISSING_CONTEXT_ENTITY: {
        "severity": Severity.ERROR,
        "area": Area.GENERAL_INSTANCE,
        "numeric_code": "001",
        "message": "Context is missing an entity child element",
        "hint": "Check the definition of the context."
    },

    ErrorCode.INVALID_DIMENSION_TYPE: {
        "severity": Severity.ERROR,
        "area": Area.GENERAL_INSTANCE,
        "numeric_code": "002",
        "message": "Dimension type '{dimension_type}' is not valid. It should either be 'explicitMember' or typedMember'.",
        "hint": "Check the segment part of the context."
    },

    ErrorCode.XML_DUPLICATE_UNIT_ID: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "000",
        "message": "Unit with ID '{id}' already exists.",
        "hint": "Check for duplicate units."
    },

    ErrorCode.XML_UNIT_ELEMENT_WITHOUT_ONE_CHILD: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "001",
        "message": "Unit with ID '{id}' must have exactly one child element. Found {child_count}.",
        "hint": "Check the children of the unit. Did you add an extra child element?"
    },

    ErrorCode.XML_DIVIDE_ELEMENT_WITHOUT_TWO_CHILDREN: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "002",
        "message": "Divide element of unit with with ID '{id}' must have exactly two children: unitNumerator and unitDenominator. Found {child_count} children, instead.",
        "hint": "Check the children of the divide element. Did you add an extra child  or miss one?"
    },

    ErrorCode.XML_INVALID_DIVIDE_ELEMENT_CHILDREN: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "003",
        "message": "Divide element of unit with ID '{id}' must have exactly two children: unitNumerator and unitDenominator. Found {child_tag} as a child.",
        "hint": "Check the children of the `divide` element. Did you misspell the name of the child?"
    },

    ErrorCode.XML_DUPLICATE_DIVIDE_ELEMENT_CHILDREN: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "004",
        "message": "The unit {id} has a divide element with two children with the same tag: {tag}. One should be 'unitNumerator' and the other 'unitDenominator'",
        "hint": "Check the children of the `divide` element. Did you forget to rename one of the children?"
    },

    ErrorCode.XML_INVALID_UNIT_ELEMENT_CHILDREN: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "005",
        "message": "Unit with ID '{id}' must have exactly one child element: 'measrue' or 'divide'. Found {child_tag} as a child.",
        "hint": "Check the child of the unit. Did you misspell the name of the child?"
    },
    
    ErrorCode.XML_MISSING_UNIT_MEASURE: {
        "severity": Severity.ERROR,
        "area": Area.XML_INSTANCE,
        "numeric_code": "006",
        "message": "Unit measure element cannot be empty.",
        "hint": "Check the unit measure. Did you misplace the text?"
    },

    # GENERAL: 000 - 099
    ErrorCode.IXBRL_DUPLICATE_ELEMENT_ID: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "001",
        "message": "ID '{id}' has already been used.",
        "hint": "Check for duplicate IDs in the instance document set."
    },

    ErrorCode.IXBRL_ELEMENT_NOT_SUPPORTED: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "002",
        "message": "Element '{tag}' is not yet supported. Ignoring for now.",
        "hint": None
    },

    # HEADER: 100 - 199
    ErrorCode.IXBRL_HEADER_ELEMENT_IN_HEAD: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "100",
        "message": "The ix:header element is not allowed in the head element.",
        "hint": "Move ix:header element to the body."
    },

    ErrorCode.IXBRL_INVALID_HEADER_CHILD: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "101",
        "message": "The ix:header element must have one of the following children: ix:hidden, ix:resources, ix:references. Found {child_tag}.",
        "hint": "Check for a misspelling in the child element."
    },

    ErrorCode.IXBRL_MORE_THAN_ONE_HIDDEN_HEADER_CHILD : {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "102",
        "message": "The ix:header element can have at most 1 ix:hidden element. Found {count}",
        "hint": "Check the ix:header element."
    },

    ErrorCode.IXBRL_MORE_THAN_ONE_RESOURCES_HEADER_CHILD : {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "103",
        "message": "The ix:header element can have at most 1 ix:resources element. Found {count}",
        "hint": "Check the ix:header element."
    },

    ErrorCode.IXBRL_NO_HEADER_ELEMENTS: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "104",
        "message": "The IXBRL Document Set must have at least one ix:header element but 0 were found.",
        "hint": "Insert an ix:header element."
    },
    
    # REFERENCES: 200 - 299
    ErrorCode.IXBRL_REFERENCES_ELEMENT_WITHOUT_CHILDREN: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "200",
        "message": "The ix:references element must have at least one child element.",
        "hint": "Check the ix:references element."
    },

    ErrorCode.IXBRL_INVALID_REFERENCES_CHILD: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "201",
        "message": "The ix:references element must have one of the following children: link:schemaRef, link:linkbaseRef. Found {children}.",
        "hint": "Check for a misspelling in the child element."
    },

    # RESOURCES: 300 - 399
    ErrorCode.IXBRL_NO_RESOURCES_ELEMENTS: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "300",
        "message": "The IXBRL Document Set must have at least one ix:resources element but 0 were found.",
        "hint": "Insert an ix:resources element inside of a ix:header element."
    },

    ErrorCode.IXBRL_INVALID_RESOURCES_CHILD: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "301",
        "message": "The ix:resources element must have one of the following children: link:roleRef, link:arcroleRef, xbrli:context, xbrli:unit. Found {child_tag}.",
        "hint": "Check for a misspelling in the child element."
    },

    ErrorCode.IXBRL_CONTEXT_WITHOUT_ID: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "360",
        "message": "Context does not have an id",
        "hint": "Set the ID attribute of the context."
    },

    ErrorCode.IXBRL_UNIT_WITHOUT_ID: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "380",
        "message": "Unit does not have an id",
        "hint": "Set the ID attribute of the unit."
    },

    ErrorCode.IXBRL_INVALID_HIDDEN_ELEMENT: {
        "severity": Severity.WARNING,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "400",
        "message": "The ix:hidden element must have one of the following children: link:roleRef, link:arcroleRef, xbrli:context, xbrli:unit. Found {child_tag}.",
        "hint": "Check for a misspelling in the children element."
    },

    ErrorCode.IXBRL_FACT_WITHOUT_CONTEXT: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "500",
        "message": "Fact with id {fact_id} does not have a context",
        "hint": "Check the `contextRef` attribute of the fact."
    },
    
    ErrorCode.IXBRL_INVALID_FACT_CONTEXT_ID: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "501",
        "message": "Fact with id {fact_id} does not have a valid context",
        "hint": "Check the `contextRef` attribute of the fact."
    },

    ErrorCode.IXBRL_FACT_WITHOUT_CONCEPT_NAME: {
        "severity": Severity.ERROR,
        "area": Area.IXBRL_INSTANCE,
        "numeric_code": "502",
        "message": "Fact with id {fact_id} does not have a concept name",
        "hint": "Check the `name` attribute of the fact."
    },

}