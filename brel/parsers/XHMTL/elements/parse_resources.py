from lxml.etree import _Element

from brel.contexts.filing_context import FilingContext
from brel.errors.error_code import ErrorCode
from brel.errors.error_instance import ErrorInstance
from brel.parsers.utils.lxml_utils import get_prefix_localname_tag

def parse_resources_elements(elements: _Element, context: FilingContext):
    relationship_elements, role_ref_elements, arcrole_ref_elements, context_elements, unit_elements = [], [], [], [], []

    for element in elements:    
        for child in element:
            child_tag = get_prefix_localname_tag(child)
            if child_tag == 'ix:relationship':
                relationship_elements.append(child)
            elif child_tag == 'link:roleRef':
                role_ref_elements.append(child)
            elif child_tag == 'link:arcroleRef':
                arcrole_ref_elements.append(child)
            elif child_tag == 'xbrli:context':
                context_elements.append(child)
            elif child_tag == 'xbrli:unit':
                unit_elements.append(child)
            else:
                error = ErrorInstance.create_error_instance(
                    ErrorCode.IXBRL_INVALID_RESOURCES_CHILD,
                    element,
                    child_tag=child_tag
                )
                
                context.get_error_repository().upsert(error)
            
    return relationship_elements, role_ref_elements, arcrole_ref_elements, context_elements, unit_elements
    