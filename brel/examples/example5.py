from brel import Filing, BrelLabelRole
from brel.utils import pprint_network
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
    filing = Filing.open("reports/coca_cola/")

    # get all components
    components = filing.get_all_components()

    # print all component names
    print("Component names:")
    for component in components:
        pre_network = component.get_presentation()
        cal_network = component.get_calculation()
        def_network = component.get_definition()

        total_network_size = 0

        if pre_network is not None:
            total_network_size += len(pre_network.get_all_nodes())
        if cal_network is not None:
            total_network_size += len(cal_network.get_all_nodes())
        if def_network is not None:
            total_network_size += len(def_network.get_all_nodes())
        
        if total_network_size == 0:
            continue

        print(f"[Size: {total_network_size}] {component.get_URI()}")

    # read the user input
    print()
    user_input = input("Enter a component name: \n")

    component_names = [component.get_URI() for component in components]
    selected_component_name = get_closest_match(user_input, component_names)

    # get the selected component
    selected_component = next(filter(lambda component: component.get_URI() == selected_component_name, components), None)
    if selected_component is None:
        print("Could not find component with name", selected_component_name)
        return

    # print the selected component's networks
    pprint_network(selected_component.get_presentation())

    pprint_network(selected_component.get_presentation())

    pprint_network(selected_component.get_calculation())

