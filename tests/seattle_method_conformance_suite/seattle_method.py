import brel
import requests
import lxml
import lxml.etree
import os.path
import rich
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

index_uri = "http://xbrlsite.com/seattlemethod/platinum-testcases/index.xml"

blacklist: list[str] = [
    "99.63",
    "99.61",
]

categories = {
    "Basic, General Tests": 16,
    "Concept Arrangement Patterns": 10,
    "Reporting Styles": 8,
    "Other": 1,
    "Invalid Logic": 4,
    "Accounting Equation States": 12,
    "Logic Rules of Thumb": 18,
    "Edge Cases": 10,
}


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
    try:
        etree = lxml.etree.parse(file_path)
        return etree
    except lxml.etree.XMLSyntaxError:
        raise Exception(f"Error parsing {uri} as XML")


index_etree = get_etree_from_uri(index_uri).getroot()

total_per_category = defaultdict(int)
correct_per_category = defaultdict(int)
false_positives_per_category = defaultdict(int)
false_negatives_per_category = defaultdict(int)

category_counter = 0
category_index = 0
for testcase_xml in index_etree.findall("testcase"):
    if category_counter >= list(categories.values())[category_index]:
        category_index += 1
        category_counter = 0

    category = list(categories.keys())[category_index]

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
        continue

    variation_xml = testcase_etree.find(f"{{{testcase_etree.nsmap[None]}}}variation")
    # get the data child of variation
    data_xml = variation_xml.find(f"{{{variation_xml.nsmap[None]}}}data")

    # go through all children in the variation
    file_names: list[str] = []
    instance_uri = None

    for child in data_xml:
        # get the uri. the uri is the relative path to the index uri joined with the tag text
        if "http" in child.text:
            file_uri = child.text
        else:
            file_uri = os.path.join(index_dir, child.text)
        # download the file

        if "instance" in child.tag:
            instance_uri = file_uri

    result_xml = variation_xml.find(f"{{{variation_xml.nsmap[None]}}}result")
    expected_result = result_xml.get("expected")

    try:
        print(instance_uri)
        filing = brel.Filing.open(instance_uri)
        actual_result = "valid"
    except Exception as e:
        actual_result = "invalid"
        print(e)

    if expected_result == actual_result:
        rich.print("[green]PASS[/green]")
        correct_per_category[category] += 1

    else:
        rich.print("[red]FAIL[/red]")
        rich.print(f"description: {testcase_description}")
        rich.print(f"expected: {expected_result}")
        rich.print(f"actual: {actual_result}")
        if actual_result == "invalid":
            false_negatives_per_category[category] += 1
        else:
            false_positives_per_category[category] += 1

    total_per_category[category] += 1
    category_counter += 1

# print summary
bar_symbol = "█"
rich.print("[bold]Summary[/bold]")
rich.print(f"[green]Correct, [yellow]False Positives, [red]False Negatives")

total_cases = sum(total_per_category.values())
total_correct = sum(correct_per_category.values())
total_false_positives = sum(false_positives_per_category.values())
total_false_negatives = sum(false_negatives_per_category.values())

rich.print(
    f"Total cases: {total_cases}, Correct: {total_correct}, False Positives: {total_false_positives}, False Negatives: {total_false_negatives}"
)

for category in categories.keys():
    total = total_per_category[category]
    correct = correct_per_category[category]
    false_positives = false_positives_per_category[category]
    false_negatives = false_negatives_per_category[category]
    rich.print(f"[bold]{category}[/bold]")
    rich.print(f"Total: {total}")
    rich.print(
        f"[green]{bar_symbol * correct}[yellow]{bar_symbol * false_positives}[red]{bar_symbol * false_negatives}"
    )

# plot the results as a bar chart
plot_categories = [
    "Basic, General Tests",
    "Concept Arrangement Patterns",
    "Reporting Styles",
    "Invalid Logic",
    "Logic Rules of Thumb",
    "Edge Cases",
]
category_names = plot_categories
df_dict = {
    "correct": [correct_per_category[category] for category in category_names],
    "false positives": [
        false_positives_per_category[category] for category in category_names
    ],
    "false negatives": [
        false_negatives_per_category[category] for category in category_names
    ],
}

df = pd.DataFrame(df_dict, index=category_names)

plt.style.use("seaborn-v0_8-darkgrid")

df.plot(
    kind="bar",
    stacked=True,
    color=["#2ca02c", "#ff7f0e", "#d62728"],
    figsize=(5, 5),
)

plt.xticks(rotation=90)
# make the y-ticks integers
plt.yticks(range(0, 21, 2))

# plt.title("Seattle Method Test Results")
plt.title("Conformance Suite Test Results")
plt.xlabel("Category")
plt.ylabel("Test case count")
# plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))

# plt.gca().yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig("docs/thesis_latex/images/seattle_method_test_results.png")
# plt.show()
