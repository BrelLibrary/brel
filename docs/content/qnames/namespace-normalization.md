<a id="brel.parsers.XML.xml_namespace_normalizer"></a>

# brel.parsers.XML.xml\_namespace\_normalizer

This module contains the XML namespace normalizer.

It is not intended to be used by the user directly. Rather, it is used by the XML parser to normalize the namespace mappings.

In XML, namespaces can be defined per element. Therefore, the same prefix can map to different urls and the same url can map to different prefixes.
It all depends on the context in which the prefix is used. From a user perspective, this is very confusing. 
When a user looks for e.g. us-gaap:Assets, he usually doesn't care if it is us-gaap's 2022 or 2023 version. 
Also, if the filing calls the prefix us-gaap1 instead of us-gaap for some contexts, then the user will have to know this and use the correct prefix.

Namespace normalizing turns the nested namespace mappings into a flat namespace mapping. It also generates redirects and renames for the prefixes.
For the example above, it would generate the following mapping:

- us-gaap -> us-gaap-2023-01-31
- redirect: us-gaap1 -> us-gaap

More precisely, it does the following:

- It groups the prefix->url mappings by their unversioned url.
- For each group, it picks the main prefix and the latest version of the url.
- For each non-main prefix, it generates a redirect to the main prefix.

Renames are generated if two completely different urls are mapped to the same prefix.
In that case, the name of the prefix is changed to a new prefix.
A rename has the following form: 

- old_url -> (old_prefix, new_prefix)

====================

- author: Robin Schmidiger
- version: 0.4
- date: 21 January 2024

====================

<a id="brel.parsers.XML.xml_namespace_normalizer.normalize_nsmap"></a>

#### normalize\_nsmap

```python
def normalize_nsmap(
        namespace_mappings: list[dict[str, str]]) -> dict[str, dict[str, str]]
```

Given a list of namespace mappings, normalize the namespace mappings and returns the normalized namespace mapping and the redirects.

A mapping is considered normalized if there is a 1:1 mapping between prefixes and urls.
If a prefix maps to multiple urls, then the latest version of the url is chosen.
If multiple prefixes map to the same url, then the shortest prefix is chosen as the main prefix.
The other prefixes are redirected to the main prefix.

**Arguments**:

- `namespace_mappings`: A list of namespace mappings.

**Returns**:

`dict`: A dictionary containing the normalized namespace mapping and the redirects.

