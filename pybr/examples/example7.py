from pybr import PyBRFiling
from pybr.networks import DefinitionNetwork, ReferenceNetwork, LabelNetwork 
from pybr.utils import pprint_network

def example7():
    filing = PyBRFiling.open("reports/coca_cola/")

    requested_link_role = "http://xbrl.sec.gov/ecd/role/TabularListsByExecutiveCategory"

    # get all pyhsical networks
    physical_networks = filing.get_all_pyhsical_networks()

    # filter the physical definition networks for the requested link role
    physical_definition_networks = filter(lambda network: isinstance(network, DefinitionNetwork) and network.get_link_role() == requested_link_role, physical_networks)

    # print the definition networks
    print("-" * 10, "PHYSICAL DEFINITION NETWORKS", "-" * 10)
    for definition_network in physical_definition_networks:
        pprint_network(definition_network)

    # get the component TabularListsByExecutiveCategory
    components = filing.get_all_components()
    component = next(filter(lambda x: x.get_URI() == requested_link_role, components), None)

    # print the definition network of the component
    print("-" * 10, "DEFINITION NETWORK OF COMPONENT", "-" * 10)
    if component is not None:
        pprint_network(component.get_definition())
    else:
        print("Component not found")
    
    # get the physical label networks
    physical_label_networks = filter(lambda network: isinstance(network, LabelNetwork), physical_networks)

    # print the label networks
    print("-" * 10, "PHYSICAL LABEL NETWORKS", "-" * 10)
    for label_network in physical_label_networks:
        pprint_network(label_network)


    # get the physical reference networks
    physical_reference_networks = filter(lambda network: isinstance(network, ReferenceNetwork), physical_networks)

    # print the reference networks
    print("-" * 10, "PHYSICAL REFERENCE NETWORKS", "-" * 10)
    for reference_network in physical_reference_networks:
        pprint_network(reference_network)
