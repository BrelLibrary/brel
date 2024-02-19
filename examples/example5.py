from brel import Filing
from brel.utils import pprint


def edit_distance(s1, s2):
    """
    Calculates the edit distance between two strings
    :param s1: str containing the first string
    :param s2: str containing the second string
    :return: int containing the edit distance between the two strings
    """
    if len(s1) < len(s2):
        return edit_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


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
