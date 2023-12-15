from brel import Filing
from brel.networks import FootnoteNetwork
from brel.utils import print_networks

filing_path = "tests/interactive_data_test_suite/conf/604-filing-semantics/604-03-xbrl-valid/"
file_short = "e60403035gd-20111231"

filing_path = "tests/interactive_data_test_suite/conf/604-filing-semantics/604-03-xbrl-valid/"
instance_filename = f"{file_short}.xml"
linkbase_filenames = [
    f"{file_short}_lab.xml",
    f"{file_short}_pre.xml",
]


for i in range(len(linkbase_filenames)):
    linkbase_filenames[i] = filing_path + linkbase_filenames[i]

filing = Filing.open(filing_path + instance_filename, linkbases=linkbase_filenames)

for network in filing.get_all_pyhsical_networks():
    if isinstance(network, FootnoteNetwork):
        print_networks.pprint_network(network)

