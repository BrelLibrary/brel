from brel import Filing
from brel.networks import FootnoteNetwork
import brel.utils

# load ete filing
filing = Filing.open("tests/end_to_end_tests/ete_filing")

# get the balance component
balance_component = filing.get_component("http://foo/role/balance")

# pprint the definition network
print(balance_component.get_definition_network() is None)

# brel.utils.pprint_network(balance_component.get_definition_network())
