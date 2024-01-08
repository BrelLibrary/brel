# Brel Examples

This page contains examples of how to use Brel.

## Example 1: Loading a filing and printing its facts

```python
from brel import Filing, pprint

# Load a filing from a file. In this case, the file is called "filing.xml".
filing = Filing.from_file("path/to/filing.xml")

# Get all the facts in the filing.
facts = filing.get_all_facts()

# Print the facts.
pprint(facts)
```