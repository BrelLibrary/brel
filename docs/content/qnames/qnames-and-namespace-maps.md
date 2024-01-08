<a id="brel.qname"></a>

# brel.qname

This module contains the QName class and the QNameNSMap class.
The QName class represents a qualified name.
The QNameNSMap class represents a namespace map.

====================

- author: Robin Schmidiger
- version: 0.6
- date: 06 January 2024

====================

<a id="brel.qname.QName"></a>

## QName Objects

```python
class QName()
```

This class represents a qualified name. Qualified names are used in XML and XBRL to identify elements.
Brel re-uses qualified names to identify report elements, types, etc. in the report.
A qualified name consists of a URI, a prefix and a local name.

- The URI identifies the namespace of the element.
- The prefix is a short string that is used to identify the namespace.
- The local name is the name of the element within the namespace.

An example of a qualified name is us-gaap:Assets.

- The URI is http://fasb.org/us-gaap/2019-01-31
- The prefix is us-gaap and acts as an abbreviation for the URI
- The local name is Assets

The [`QName`](#brel.qname.QName) class is closely related to the [`QNameNSMap`](#brel.qname.QNameNSMap) class. The QNameNSMap class is used to map prefixes to URIs and vice versa.
When creating a QName, sometimes either the prefix or the URI is unknown. In this case, the QNameNSMap class is used to find the missing information.
There is usually only one QNameNSMap object per report. It is created when the report is created and then passed to the QName constructor.

<a id="brel.qname.QNameNSMap"></a>

## QNameNSMap Objects

```python
class QNameNSMap()
```

This class represents a namespace map used to map prefixes to URIs and vice versa.
It is used by the [`QName`](#brel.qname.QName) class to create QNames from strings.
It requires a 1:1 mapping between prefixes and URIs.

A QNameNSMap introduces two concepts to achieve this: prefix redirects and prefix renames.

**Prefix redirects**

For many reports, it is possible that the same namespace is used with different prefixes.
For example, the namespace http://fasb.org/us-gaap/2020 is used with the prefixes us-gaap and us-gaap-ci.
This is not allowed in Brel. So one of the prefixes must be redirected to the other.
In case of the example above, the prefix us-gaap-ci must be redirected to us-gaap.
This can be done as follows:
```
nsmap.add_redirect("us-gaap-ci", "us-gaap")
```

**Prefix renames**

Sometimes, the same prefix is used for different namespaces.
For example, the prefix 'types' is used for the namespaces http://fasb.org/us-types/2020 and http://fasb.org/uk-types/2020.
This is not allowed in Brel. So one of the prefixes must be renamed.
In case of the example above, the prefix 'types' could be renamed to 'us-types' or 'uk-types'.
This can be done as follows:
```
nsmap.rename("http://fasb.org/us-types/2020", "us-types")
```

Now whenever a QName is created with the prefix 'namespaces', the prefix will be replaced with 'us-types'.

