from copy import deepcopy
from typing import Dict, Set

from lxml.etree import _Element
from lxml import etree
from brel.brel_context import Context
from brel.brel_fact import Fact
from brel.parsers.XHMTL.elements.parse_continuation_chain import extract_relevant_content_from_continuation_chain
from brel.parsers.XHMTL.xhtml_parse_transformation_registry import parse_non_numerical_fact_value
from brel.parsers.utils.lxml_utils import get_str_attribute_optional

def convert_escaped_characters(text: str) -> str:
    snippets_to_replace = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }

    for actual, escaped in snippets_to_replace.items():
        text = text.replace(actual, escaped)
    
    return text

def convert_escaped_characters_recursive(content: _Element) -> _Element:
    if content.text is not None:
        content.text = convert_escaped_characters(content.text)
    
    if content.tail is not None:
        content.tail = convert_escaped_characters(content.tail)
    
    for child in content:
        convert_escaped_characters_recursive(child)

def escape_content(content: _Element) -> str:
    convert_escaped_characters_recursive(content)

    text_nodes = []
    text_nodes.append(content.text if content.text else "")

    for child in content: 
        child = etree.tostring(child, encoding='unicode')
        text_nodes.append(child)
    
    full_text = "".join(text_nodes)
    return full_text

def extract_text_content(content: _Element) -> str:
    all_text_nodes = []
    all_text_nodes.append(content.text if content.text else "")

    for child in content:
        child_text = extract_text_content(child)
        all_text_nodes.append(child_text if child_text else "")
        all_text_nodes.append(child.tail if child.tail else "")

    return "".join(all_text_nodes)

def parse_non_numeric_fact_element(fact_element: _Element, context: Context, continuation_chain: list[_Element], taken_ids=Set[str]) -> Fact:
    id = get_str_attribute_optional(fact_element, "id")

    if id is not None:
        if id in taken_ids:
            raise ValueError(f"ID '{id}' has already been used.")
        
        taken_ids.add(id)

    escape = get_str_attribute_optional(fact_element, "escape")
    
    if escape and escape not in ["true", "false"]:
        raise ValueError(f"Fact with id '{get_str_attribute_optional(fact_element, 'id')}' has an escape attribute with value '{escape}', which is not 'true' or 'false'.")
    
    relevant_content = extract_relevant_content_from_continuation_chain(fact_element, continuation_chain)
    
    fact_value = None
    if escape == "true":
        fact_value = escape_content(relevant_content)
    else:
        fact_value = extract_text_content(relevant_content)
    
    format = get_str_attribute_optional(fact_element, "format")
    parsed_value = parse_non_numerical_fact_value(fact_value, format)
    
    return Fact(context, parsed_value, id)

if __name__ == "__main__":
    data = '<ix:nonNumeric id="1" xmlns:ix="http://www.xbrl.org/2003/instance" escape="false">abcd &amp; <ix:exclude><ix:nonFraction>22</ix:nonFraction>44</ix:exclude> <ix:nonNumeric>This should still &lt; b &gt;be there as <xml:b>text</xml:b></ix:nonNumeric> 33 <xml:c> abb </xml:c> ccc <ix:exclude> ciao </ix:exclude> abeee</ix:nonNumeric>'
    root = etree.fromstring(data)
    fact = parse_non_numeric_fact_element(
        root,
        Context('1'),
        []
    )
    print(fact.get_value())