from pybr import PyBRFiling
from pybr.networks import DefinitionNetwork
from pybr.utils import pprint_network

def example7():
    filing = PyBRFiling.open("reports/coca_cola/")

    # get all pyhsical networks
    networks = filing.get_all_pyhsical_networks()

    # filter the definition networks
    definition_networks = filter(lambda network: isinstance(network, DefinitionNetwork), networks)

    # print the definition networks
    for definition_network in definition_networks:
        pprint_network(definition_network)