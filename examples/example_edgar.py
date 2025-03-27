from brel import Filing, utils


microsoft_cik = "789019"
apple_cik = "320193"

# get the 10-K filing for Microsoft and the 10-Q filing for Apple
# print the first 10 facts for each filing
microsoft_filing = utils.open_edgar("789019", "10-K")
utils.pprint(microsoft_filing.get_all_facts()[:10])

apple_filing = utils.open_edgar("320193", "10-Q", "2023-08-04")
utils.pprint(apple_filing.get_all_facts()[:10])
