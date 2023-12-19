from brel import Filing, Component

def example4():
    filing = Filing.open("reports/ko/")

    components = filing.get_all_components()

    components_slice_size = 10
    print(f"First {components_slice_size} Components:")

    for component in components[:components_slice_size]:
        print()
        print(component.get_URI())
        print(component.get_info())
