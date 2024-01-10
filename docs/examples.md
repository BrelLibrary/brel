# Brel Examples

This page contains examples of how to use Brel.

## Example 1: Loading a filing and printing its facts

```python
from brel import Filing, pprint

# Load a filing from a file. In this case, the file is called "filing.xml".
filing = Filing.from_file("path/to/filing.xml")

# Get all the facts in the filing. Take the first 10 facts.
facts = filing.get_all_facts()
first_10_facts = facts[:10]

# Print the facts.
pprint(first_10_facts)
```

## Example 2: Loading a filing and printing its facts where the concept is "us-gaap:Assets"

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
