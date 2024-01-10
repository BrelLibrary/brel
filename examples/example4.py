from brel import Filing, Component, pprint


def example4():
    # MAKE SURE TO CHANGE THIS TO THE PATH OF THE FILING YOU WANT TO USE
    print(
        "MAKE SURE TO CHANGE THE PATH IN EXAMPLE1.PY TO THE PATH OF THE FILING YOU WANT TO USE"
    )
    filing = Filing.open("reports/report.zip")

    # get all components
    components = filing.get_all_components()

    # take the first 10 components
    components_slice_size = 10
    print(f"First {components_slice_size} Components:")

    for component in components[:components_slice_size]:
        # print the component
        print()
        print(component.get_URI())
        print(component.get_info())

        presentation_network = component.get_presentation_network()
        if presentation_network:
            print("Presentation Network:")
            pprint(presentation_network)

        definition_network = component.get_definition_network()
        if definition_network:
            print("Definition Network:")
            pprint(definition_network)

        calculation_network = component.get_calculation_network()
        if calculation_network:
            print("Calculation Network:")
            pprint(calculation_network)


if __name__ == "__main__":
    example4()
