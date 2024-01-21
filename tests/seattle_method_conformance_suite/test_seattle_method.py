import brel
import requests
import lxml
import lxml.etree
import os.path
import rich

index_uri = "http://xbrlsite.com/seattlemethod/platinum-testcases/index.xml"

blacklist = [
    "helloworld-using-dim",  # Contains html
    "lorem-ipsum-all-patterns",  # Contains html
    "dimensions-ppe",  # Contains html
    "TestCase-logic",  # Contains html
    "TestCase-ae-BS1",  # Contains html
    "TestCase-sfac6-BS1-IS1",  # Contains html
    "TestCase-sfac8-reference",  # Contains html
    "TestCase-common-reference",  # Contains html
    "TestCase-mini-reference",  # Contains html
    "TestCase-proof-reference",  # Contains html
    "TestCase-xasb-reference",  # Contains html
    "TestCase-aasb1060-reference",  # Contains html
    "TestCase-helloworld",  # Contains html
    "95",  # Contains html,
    "TestCase-fundamental-inconsistency",  # Contains html
]


def make_cache_dir():
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir


def make_dir_recursive(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def file_name_from_uri(uri: str) -> str:
    cache_dir = make_cache_dir()
    # get the index uri dir
    index_dir = os.path.dirname(index_uri)

    # remove the index dir path from the uri path
    file_name = os.path.relpath(uri, index_dir)

    # make the file path
    file_path = os.path.join(cache_dir, file_name)
    return file_path


def get_etree_from_uri(uri: str) -> lxml.etree._ElementTree:
    # get the file path
    file_path = file_name_from_uri(uri)

    # if the file does not exist, download it
    if not os.path.exists(file_path):
        # make the dirs if they don't exist
        make_dir_recursive(os.path.dirname(file_path))

        response = requests.get(uri)
        with open(file_path, "wb") as f:
            f.write(response.content)
    # return the etree
    etree = lxml.etree.parse(file_path)
    return etree


# index_response = requests.get(index_uri)
# index_etree: lxml.etree._Element = lxml.etree.fromstring(index_response.content)
index_etree = get_etree_from_uri(index_uri).getroot()

total_tests = 0
total_correct = 0
total_skipped = 0
false_positives = 0
false_negatives = 0
correct = 0

for testcase_xml in index_etree.findall("testcase"):
    total_tests += 1

    uri = testcase_xml.get("uri")

    # get the dir path of the index uri
    index_dir = os.path.dirname(index_uri)
    testcase_uri = os.path.join(index_dir, uri)

    testcase_etree = get_etree_from_uri(testcase_uri).getroot()

    testcase_name = testcase_etree.get("name")
    testcase_description = testcase_etree.get("description")

    rich.print(f"[bold]{testcase_name}[/bold]")

    # check if there is a blacklist-item that is part of the uri
    if any([item in uri for item in blacklist]):
        rich.print("[yellow]SKIPPED[/yellow]")
        total_skipped += 1
        continue

    variation_xml = testcase_etree.find(
        f"{{{testcase_etree.nsmap[None]}}}variation"
    )
    # get the data child of variation
    data_xml = variation_xml.find(f"{{{variation_xml.nsmap[None]}}}data")

    # go through all children in the variation
    file_names: list[str] = []
    for child in data_xml:
        # get the uri. the uri is the relative path to the index uri joined with the tag text
        file_uri = os.path.join(index_dir, child.text)
        # download the file
        get_etree_from_uri(file_uri)

        # check if the tag is linkbase or instance
        if "linkbase" in child.tag or "instance" in child.tag:
            # add the filename to the list
            # prepend the file name if the "readMeFirst" attribute is set "true"
            if child.get("readMeFirst") == "true":
                file_names.insert(0, file_name_from_uri(file_uri))
            else:
                file_names.append(file_name_from_uri(file_uri))

    # get the expected result
    result_xml = variation_xml.find(f"{{{variation_xml.nsmap[None]}}}result")
    expected_result = result_xml.get("expected")

    try:
        filing = brel.Filing.open(*file_names)
        actual_result = "valid"
    except Exception as e:
        actual_result = "invalid"

    if expected_result == actual_result:
        rich.print("[green]PASS[/green]")
        total_correct += 1

    else:
        rich.print("[red]FAIL[/red]")
        rich.print(f"description: {testcase_description}")
        rich.print(f"expected: {expected_result}")
        rich.print(f"actual: {actual_result}")
        if actual_result == "invalid":
            false_negatives += 1
        else:
            false_positives += 1

rich.print("[bold]Summary[/bold]")
rich.print(f"Total tests: {total_tests}")
rich.print(
    f"[green]Correct, [yellow]False Positives, [red]False Negatives, [grey37]Skipped"
)

bar_symbol = "█"
rich.print(
    f"[green]{bar_symbol * total_correct}[yellow]{bar_symbol * false_positives}[red]{bar_symbol * false_negatives}[grey37]{bar_symbol * total_skipped}"
)

test_accuracy = total_correct / (
    total_correct + false_positives + false_negatives
)
rich.print(f"Test accuracy: {test_accuracy:.2%}")

test_precision = total_correct / (total_correct + false_positives)
rich.print(f"Test precision: {test_precision:.2%}")

test_recall = total_correct / (total_correct + false_negatives)
rich.print(f"Test recall: {test_recall:.2%}")
