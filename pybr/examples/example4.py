from pybr import PyBRFiling, PyBRComponent

def example4():
    filing = PyBRFiling.open("reports/coca_cola/")

    components = filing.get_all_components()

    components_slice_size = 10
    print(f"First {components_slice_size} Components:")

    for component in components[:components_slice_size]:
        print()
        print(component.get_id())
        print(component.get_info())
