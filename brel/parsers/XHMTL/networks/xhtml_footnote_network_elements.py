from lxml.etree import _Element
from typing import Dict, List, Set


class XHTMLFootnoteNetworkElements:
    def __init__(
        self,
        footnote_elements: List[_Element],
        continuation_chains: Dict[_Element, List[_Element]],
        relationship_elements: List[_Element],
        role_ref_elements: List[_Element],
        arcrole_ref_elements: List[_Element],
        taken_ids: Set[str],
    ):
        self.footnote_elements: List[_Element] = footnote_elements
        self.continuation_chains: Dict[_Element, List[_Element]] = continuation_chains
        self.relationship_elements: List[_Element] = relationship_elements
        self.role_ref_elements: List[_Element] = role_ref_elements
        self.arcrole_ref_elements: List[_Element] = arcrole_ref_elements
        self.taken_ids: Set[str] = taken_ids
