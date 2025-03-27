# Brel Examples

This page contains examples of how to use Brel.

<!-- Note: Brel does not contain any filings. You will have to download them yourself. You can find some example filings [here](https://www.sec.gov/edgar/searchedgar/companysearch). -->

Note: Make sure you have a working internet connection to download filings from the SEC's EDGAR database.

<!-- The following steps are required to download a filing and load it into Brel: -->

<!-- 1. Search for the filing on the SEC website.
2. Under the "10-K (Annual Report) and 10-Q (Quarterly Report)" click on the "Filing" button.
3. In the "Data Files" section, download all the ".xsd" and ".xml" files and place them in a folder (e.g. "path/to/filing").
4. Start python and import Brel.
5. Load the filing using `Filing.open("path/to/filing")`. -->

Brel provides a helper function to load filings from the [SEC's EDGAR database](https://www.sec.gov/edgar/searchedgar/cik.htm). This function allows you to load filings by specifying the company's CIK, the form type, and the date of the filing.

## Example 1: Loading a filing and printing its facts

```python
from brel import Filing, pprint
from brel.utils import open_edgar

# Loads Apples 10-Q filing from Q4 2023
filing = open_edgar(cik="320193", form="10-Q", date="2023-12-30")

# Get all the facts in the filing. Take the first 3 facts.
facts = filing.get_all_facts()
first_3_facts = facts[:3]

# Print the facts.
pprint(first_3_facts)
```

Notes: 
- The format of the date is "YYYY-MM-DD". If no date is specified, the most recent filing will be downloaded.
- The date refers to the date on the report, not the date the report was filed.
- `open_edgar` supports the following form types: "10-K", "10-Q", and "8-K". 

## Example 2: Loading a filing and printing its facts where the concept is "us-gaap:Assets"

In case you have a filing on your local machine or you have an uri to a filing in XML format, you can load it using the `Filing.open` method.

```python
from brel import Filing, pprint

# Load a filing from a file. In this case, the file is called "filing.xml".
filing = Filing.from_file("path/to/filing.xml")

# Get the concept "us-gaap:Assets".
assets_concept = filing.get_concept("us-gaap:Assets")

# Get all the facts in the filing where the concept is "us-gaap:Assets".
assets_facts = filing.get_facts_by_concept(assets_concept)

# Print the facts.
pprint(assets_facts)
```

Note: Brel currently only supports the XML format for filings. It will reject any other format.

## Example 3: Loading the cover page of a filing and printing its presentation network

```python
from brel import Filing, pprint

# Load a filing from a file. In this case, the file is called "filing.zip".
# Note that the zip file contains the filing's instance as well as its linkbases.
filing = Filing.from_zip("path/to/filing.zip")

# Get the cover page component.
cover_page_uri = "http://www.mycompany.com/roles/coverpage"
cover_page_component = filing.get_component(cover_page_uri)

if cover_page_component is None:
    raise Exception(f"Could not find component with URI {cover_page_uri}")

# Get the presentation network of the cover page component and print it.
presentation_network = cover_page_component.get_presentation_network()
if presentation_network is not None:
    pprint(presentation_network)
```

## Additional Examples

You can find additional examples in the ["examples" folder of the repository](https://github.com/PapediPoo/Brel/tree/main/examples).

Make sure that in the examples, you replace the paths to the filings with the paths to your filings.