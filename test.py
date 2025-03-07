import brel
import brel.utils

# filing = brel.utils.open_edgar('0000789019', "10-Q")
filing = brel.Filing.open("../nvda/", mode="xhtml")

print(filing.get_all_concepts()[0])