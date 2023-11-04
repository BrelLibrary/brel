from pybr import PyBRFiling, PyBRLabelRole
from pybr.utils import pprint_network, pprint_network_node
from random import sample
from editdistance import eval as edit_distance

def get_closest_match(target: str, candidates: list[str]) -> str:
    """
    Finds and returns the candidate with the smallest edit distance to the target
    Note: this function is case insensitive. For the candidates, only the last part of the URI is used.
    @param target: str containing the target string
    @param candidates: list[str] containing the candidates
    @return: str containing the candidate with the smallest edit distance to the target
    """
    return min(candidates, key=lambda candidate: edit_distance(target.upper(), candidate.split("/")[-1].upper()))

def example5():
    filing = PyBRFiling.open("reports/aapl/")

    # get all components
    components = filing.get_all_components()

    # print all component names
    print("Component names:")
    for component in components:
        pre_network = component.get_presentation()

        if pre_network is None:
            continue

        print(f"[SIZE: {len(pre_network.get_all_nodes()):3}] {component.get_URI()}")

    # read the user input
    print()
    user_input = input("Enter a component name: \n")

    component_names = [component.get_URI() for component in components]
    selected_component_name = get_closest_match(user_input, component_names)

    # get the selected component
    selected_component = filter(lambda component: component.get_URI() == selected_component_name, components).__next__()

    # print the selected component's presentation network

    # short version for printing the network
    # maybe needs a preferred lang arg as well
    # pprint_network(selected_component.get_presentation())

    # long version where you specify the preferred label role and whether or not to print the report element type
    pprint_network(selected_component.get_presentation(), label_role=PyBRLabelRole.STANDARD_LABEL, print_report_element_type=True)

