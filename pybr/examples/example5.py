from pybr import PyBRFiling, PyBRLabelRole
from pybr.utils import pprint_network
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
    filing = PyBRFiling.open("reports/coca_cola/")

    # get all components
    components = filing.get_all_components()

    # print all component names
    # TODO: uncomment
    print("Component names:")
    for component in components:
        pre_network = component.get_presentation()
        cal_network = component.get_calculation()
        def_network = component.get_definition()

        if pre_network is None:
            pre_network_size = 0
        else:
            pre_network_size = len(pre_network.get_all_nodes())
        if cal_network is None:
            cal_network_size = 0
        else:
            cal_network_size = len(cal_network.get_all_nodes())
        if def_network is None:
            def_network_size = 0
        else:
            def_network_size = len(def_network.get_all_nodes())
        
        if pre_network_size == 0 and cal_network_size == 0 and def_network_size == 0:
            continue

        # TODO: uncomment
        print(f"[PSIZE: {pre_network_size}, CSIZE: {cal_network_size}, DSIZE: {def_network_size}] {component.get_URI()}")

    # read the user input
    print()
    # TODO: uncomment
    # user_input = input("Enter a component name: \n")
    # user_input = "FAIRVALUEMEASUREMENTSAssetsandLiabilitiesMeasuredatFairValueonaRecurringBasisDetails"
    # user_input = "OTHERCOMPREHENSIVEINCOMEAdjustmentReclassifiedtoIncomeDetails"
    user_input = "DOCUMENTANDENTITYINFORMATION"

    component_names = [component.get_URI() for component in components]
    selected_component_name = get_closest_match(user_input, component_names)

    # get the selected component
    selected_component = filter(lambda component: component.get_URI() == selected_component_name, components).__next__()

    # print the selected component's presentation network

    # short version for printing the network
    # maybe needs a preferred lang arg as well
    # pprint_network(selected_component.get_presentation())

    # long version where you specify the preferred label role and whether or not to print the report element type
    # pprint_network(selected_component.get_presentation())

    # print("is valid?", selected_component.get_calculation().validate(filing))
    # pprint_network(selected_component.get_calculation())

    pprint_network(selected_component.get_definition())
