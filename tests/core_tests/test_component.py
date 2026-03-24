"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""
from brel.brel_filing import Filing


def test_component_getters():
    filing = Filing.open("tests/end_to_end_tests/hand_made_report/ete_filing")
    balance_component = filing.get_component("http://foo/role/balance")

    assert (
        balance_component.get_URI() == "http://foo/role/balance"
    ), f"URI is {balance_component.get_URI()}, expected http://foo/role/balance"
