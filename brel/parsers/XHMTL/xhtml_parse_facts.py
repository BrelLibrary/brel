import json
from bs4 import BeautifulSoup


def parse_facts_from_xhtml(ixbrl: BeautifulSoup) -> dict[str, str]:
    """
    Parse facts from an xhtml file.
    """
    # get all the elements with the tag ix:nonFraction or ix:nonNumeric
    ixbrlelements = ixbrl.find_all(["ix:nonfraction", "ix:nonnumeric", "ix:continuation"], recursive=True)
    print(ixbrlelements)

    # convert the elements to a list of dictionary with all its attributes
    nonFraction_dict = []
    i = 0
    for element in ixbrlelements:
        nonFraction_dict.append({})
        nonFraction_dict[i]["VALUE"] = element.get_text()
        for key, value in element.attrs.items():
            nonFraction_dict[i][key] = value
        i += 1

    return nonFraction_dict