# Loading a filing from EDGAR

Brel provides a helper function to load filings from the [SEC's EDGAR database](https://www.sec.gov/edgar/searchedgar/cik.htm). This function allows you to load filings by specifying the company's CIK, the form type, and the date of the filing.

The following steps are required to download a filing from EDGAR and load it into Brel:

1. Search for the company's CIK on the [SEC website](https://www.sec.gov/edgar/searchedgar/cik.htm).
2. Specify if you want to download the 10-K, 10-Q, or 8-K filings.
3. (optional) Specify the date of the filing. If not specified, the most recent filing will be downloaded.

## Example 1: Loading a filing and printing its facts

Filings can be directly loaded from EDGAR using the `brel.utils.open_edgar` function. The following example loads the 10-K filing for Apple Inc. in 2020 and prints the first 10 facts.

```python
from brel.utils import open_edgar, pprint

# Load a filing from EDGAR. In this case, the CIK is 320193 and the form is 10-K
filing = open_edgar(cik="320193", form="10-K", year=2020)
first_10_facts = filing.get_all_facts()[:10]
pprint(first_10_facts)
```

## Example 2: Loading a filing with a date

The following example loads the 10-K filing for Apple Inc. on the 30th of September 2023 and prints the first 10 facts.

The format of the date is "YYYY-MM-DD".
Therefore, the date "30th of September 2023" is "2023-09-30".

**Important**: If Brel does not find the filing for the given date, it will raise a `ValueError`.
Also, the date refers to the date on the report, not the date the report was filed.

```python
from brel.utils import open_edgar, pprint

# Load a filing from EDGAR. 
# - CIK is 320193
# - form is 10-K
# - date is the 30th of September, 2023.
filing = open_edgar(cik="320193", form="10-K", date="2023-09-30")
```
