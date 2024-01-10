from brel import Filing
from brel.utils import pprint
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
    return min(
        candidates,
        key=lambda candidate: edit_distance(
            target.upper(), candidate.split("/")[-1].upper()
        ),
    )


def example5():
    # MAKE SURE TO CHANGE THIS TO THE PATH OF THE FILING YOU WANT TO USE
    print(
        "MAKE SURE TO CHANGE THE PATH IN EXAMPLE1.PY TO THE PATH OF THE FILING YOU WANT TO USE"
    )
    filing = Filing.open("reports/report.zip")

    # get all components
    components = filing.get_all_components()

    # print all component names
    print("Component names:")
    for component in components:
        pre_network = component.get_presentation_network()
        cal_network = component.get_calculation_network()
        def_network = component.get_definition_network()

        total_network_size = ""

        if pre_network is not None:
            total_network_size += "p" + str(len(pre_network.get_all_nodes()))
        if cal_network is not None:
            total_network_size += "c" + str(len(cal_network.get_all_nodes()))
        if def_network is not None:
            total_network_size += "d" + str(len(def_network.get_all_nodes()))

        if total_network_size == "":
            continue

        print(f"[Size: {total_network_size}] {component.get_URI()}")

    non_root_lineitems = []
    for component in components:
        defi_network = component.get_definition_network()
        if defi_network is None:
            continue

        for node in defi_network.get_all_nodes():
            if (
                "LineItems"
                in node.get_report_element().get_name().resolve()
                # and node != defi_network.get_root()
            ):
                non_root_lineitems.append(node)

    print("Non root lineitems:" + str(len(non_root_lineitems)))

    # read the user input
    print()
    user_input = input("Enter a component name: \n")

    component_names = [component.get_URI() for component in components]
    selected_component_name = get_closest_match(user_input, component_names)

    # get the selected component
    selected_component = next(
        filter(
            lambda component: component.get_URI() == selected_component_name, components
        ),
        None,
    )
    if selected_component is None:
        print("Could not find component with name", selected_component_name)
        return

    # print the selected component's networks
    if selected_component.get_presentation_network() is not None:
        print("Presentation Network:")
        pprint(selected_component.get_presentation_network())

    if selected_component.get_definition_network() is not None:
        print("Definition Network:")
        pprint(selected_component.get_definition_network())

    if selected_component.get_calculation_network() is not None:
        print("Calculation Network:")
        pprint(selected_component.get_calculation_network())


if __name__ == "__main__":
    example5()
