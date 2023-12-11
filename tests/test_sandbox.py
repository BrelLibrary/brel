import lxml
import lxml.etree

from brel import Filing

filing_path = "tests/interactive_data_test_suite/conf/604-filing-semantics/604-03-xbrl-valid/"
instance_filename = "e60403012gd-20111231.xml"
linkbase_filenames = [
    "e60403012gd-20111231_lab.xml",
    "e60403012gd-20111231_pre.xml",
    "e60403012gd-20111231_def.xml"
]

for i in range(len(linkbase_filenames)):
    linkbase_filenames[i] = filing_path + linkbase_filenames[i]

filing = Filing.open(filing_path + instance_filename, linkbases=linkbase_filenames)
