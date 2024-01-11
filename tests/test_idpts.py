"""
This module runs the interactive data test suite created by the SEC.

@author: Robin Schmidiger
@version: 0.0.3
@date: 15 December 2023
"""

import lxml
import lxml.etree
from rich import print

from brel import Filing


# def prepend_path_prefix(filename):
#     return idpts_testcases_folder + filename

# testcase_filenames = list(map(prepend_path_prefix, testcase_filenames))

# testcase_filenames = ['605-instance-syntax/605-01-entity-identifier-scheme/605-01-entity-identifier-scheme-testcase.xml']
# whitelist: list[str] = [
#     "603-instance-syntax",
#     "604-filing-semantics",
#     "605-instance-syntax",
#     "607-schema-syntax",
#     "609-linkbase-syntax",
#     "610-label-syntax",
#     "612-presentation-syntax",
#     "614-calculation-syntax",
#     "616-definition-syntax",
#     "618-reference-syntax",
#     "622-only-supported-locations",
# ]
whitelist: list[str] = ["604"]

blacklist: list[str] = []


def filter_testcase_files(testcase_filename):
    if any(map(lambda x: x in testcase_filename, whitelist)):
        return True
    return False


def filter_testcase_by_name(testcase_name: str) -> bool:
    if any(map(lambda x: x in testcase_name, blacklist)):
        return False
    return True


def test_idpts():
    idpts_testcases_folder = "tests/interactive_data_test_suite/conf/"
    idpts_testcases_filename = "testcases.xml"

    testcases_etree = lxml.etree.parse(
        idpts_testcases_folder + idpts_testcases_filename
    )
    testcase_elements = testcases_etree.xpath("//testcase")

    testcase_filenames = [
        testcase_element.get("uri") for testcase_element in testcase_elements
    ]

    testcase_filenames = list(
        filter(filter_testcase_files, testcase_filenames)
    )

    print("Testcase files")
    for testcase_filename in testcase_filenames:
        print(f"> {testcase_filename}")

    for testcase_filename in testcase_filenames:
        testcase_etree = lxml.etree.parse(
            idpts_testcases_folder + testcase_filename
        )
        testcase_elem = testcase_etree.getroot()

        # creator = testcase_elem.find("{*}creator")
        # if creator is not None:
        #     creator_name = creator.find("{*}name")
        #     creator_email = creator.find("{*}email")
        #     if creator_name is not None and creator_email is not None:
        #         print(f"creator: {creator_name.text} ({creator_email.text})")

        # print the test nr
        test_nr = testcase_elem.find("{*}number")
        test_name = testcase_elem.find("{*}name")
        if test_nr is not None and test_name is not None:
            print(f"Running test {test_name.text} ({test_nr.text})")

        variations = testcase_elem.findall("{*}variation")
        for variation in variations:
            # print the variation id and name
            variation_id = variation.get("id")
            variation_name = variation.find("{*}name")
            if variation_name is not None:
                print(f"variation: {variation_name.text} ({variation_id})")

            # get filenames relevant for this variation
            data = variation.find("{*}data")

            instance_filename = data.find("{*}instance").text
            linkbase_filenames = [
                linkbase.text for linkbase in data.findall("{*}linkbase")
            ]

            # skip the testcase if any of the instance of a linkbase is not xml
            if not instance_filename.endswith(".xml"):
                continue

            if not all(map(lambda x: x.endswith(".xml"), linkbase_filenames)):
                continue

            testcase_folder = testcase_filename.rsplit("/", 1)[0]

            path_prefix = idpts_testcases_folder + testcase_folder + "/"

            def prepend_path_prefix(filename):
                return path_prefix + filename

            instance_filename = prepend_path_prefix(instance_filename)
            linkbase_filenames = [
                prepend_path_prefix(linkbase_filename)
                for linkbase_filename in linkbase_filenames
            ]

            # get the expected results
            result = variation.find("{*}result")
            expected_result = result.get("expected", "error")

            # run the test
            text_exception: Exception | None = None

            try:
                filing = Filing.open(instance_filename, *linkbase_filenames)
                print(f"> No exception raised.")
            except Exception as e:
                # print(f"Exception: {e}")
                print(f"> Exception raised: {e}")
                text_exception = e

            if (
                expected_result == "error" or expected_result == "invalid"
            ) and text_exception is None:
                print(
                    f"[bold red][!!! FAIL !!!][/bold red]",
                    f"expected error, but none was raised.",
                )
            elif expected_result == "valid" and text_exception is not None:
                print(
                    f"[bold red][!!! FAIL !!!][/bold red]",
                    f"expected no error, but got {text_exception}",
                )


if __name__ == "__main__":
    test_idpts()
