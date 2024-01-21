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

<a id="brel.qname.QName.__init__"></a>

#### \_\_init\_\_

```python
def __init__(uri: str, prefix: str, local_name: str, nsmap: "QNameNSMap")
```

Creates a QName object.

Note that this constructor changes the prefix if there is a prefix redirect in the [`QNameNSMap`](#brel.qname.QNameNSMap).

**Arguments**:

- `uri`: str containing the URI. Must be a valid URL
- `prefix`: str containing the prefix
- `local_name`: str containing the local name
- `nsmap`: QNameNSMap containing the namespace map

**Raises**:

- `ValueError`: if there is a conflict with the namespace map

<a id="brel.qname.QName.get_URL"></a>

#### get\_URL

```python
def get_URL() -> str
```

**Returns**:

`str`: containing the URI

<a id="brel.qname.QName.get_prefix"></a>

#### get\_prefix

```python
def get_prefix() -> str
```

**Returns**:

`str`: containing the prefix

<a id="brel.qname.QName.get_local_name"></a>

#### get\_local\_name

```python
def get_local_name() -> str
```

**Returns**:

`str`: containing the local name

<a id="brel.qname.QName.get_nsmap"></a>

#### get\_nsmap

```python
def get_nsmap() -> "QNameNSMap"
```

**Returns**:

`QNameNSMap`: containing the namespace map.

<a id="brel.qname.QName.get"></a>

#### get

```python
def get() -> str
```

**Returns**:

`str`: representation of the qualified name.
it does not substitute the prefix with the URI.

example: us-gaap:Assets

<a id="brel.qname.QName.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

**Returns**:

`str`: representation of the qualified name.
Functionally equivalent to QName.get()

<a id="brel.qname.QName.__eq__"></a>

#### \_\_eq\_\_

```python
def __eq__(__value: object) -> bool
```

Checks if the QName self is equal to the QName __value.

Two QNames are equal if
- the local name is equal
- the prefix is equal

Note that the URI is not considered when checking for equality.
This is because Brel does not allow two completely different URIs to map to the same prefix.
Two URIs are completely different if they are not versions of the same URI.
Example:
- http://www.xbrl.org/2003/instance and http://www.xbrl.org/2020/instance are versions of the same URI.
- http://www.xbrl.org/2003/instance and http://www.xbrl.org/2003/taxonomy are not versions of the same URI.

**Arguments**:

- `__value`: object containing the QName to compare with.

**Returns**:

`bool`: True if __value is a QName and it is equal to self, False otherwise.

<a id="brel.qname.QName.__hash__"></a>

#### \_\_hash\_\_

```python
def __hash__() -> int
```

**Returns**:

`int`: containing the hash of the QName

<a id="brel.qname.QName.resolve"></a>

#### resolve

```python
def resolve() -> str
```

produces the clark notation of the qualified name

it substitutes the prefix with the URI

example: {http://www.xbrl.org/2003/instance}Assets

**Returns**:

`str`: containing the clark notation of the qualified name

<a id="brel.qname.QName.from_string"></a>

#### from\_string

```python
@classmethod
def from_string(cls, qname_string: str, nsmap: "QNameNSMap") -> "QName"
```

Creates a QName from a string representation of a QName

The string representation must be in one of the following formats:
- {URL}local_name
- prefix:local_name
Furthermore, The prefix and the URL must be known. So there must be an entry in the namespace map for the prefix and the URL.

**Arguments**:

- `qname_string`: str containing the string representation of the QName
- `nsmap`: QNameNSMap containing the namespace map

**Raises**:

- `ValueError`: if the string representation is not valid or if the prefix or the URL is not known

**Returns**:

`QName`: the QName created from the string representation

<a id="brel.qname.QName.is_str_qname"></a>

#### is\_str\_qname

```python
@classmethod
def is_str_qname(cls, qname_string: str, nsmap: "QNameNSMap") -> bool
```

Checks if a string represents a QName and could be parsed by QName.from_string()

**Arguments**:

- `qname_string`: str containing the string representation of the QName
- `nsmap`: QNameNSMap containing the namespace map

**Returns**:

`bool`: True if the string represents a QName, False otherwise

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

<a id="brel.qname.QNameNSMap.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Creates a QNameNSMap object

<a id="brel.qname.QNameNSMap.add_to_nsmap"></a>

#### add\_to\_nsmap

```python
def add_to_nsmap(url: str, prefix: str) -> None
```

Adds a prefix to the namespace map

**Arguments**:

- `url`: str containing the URL
- `prefix`: str containing the prefix

**Raises**:

- `ValueError`: if the URL/prefix is already in the namespace map, but mapped to a different prefix/URL than the one provided

<a id="brel.qname.QNameNSMap.add_redirect"></a>

#### add\_redirect

```python
def add_redirect(redirect_from: str, redirect_to: str) -> None
```

Adds a prefix redirect to the namespace map.

When creating a new QName, the redirect_from prefix will be replaced with the redirect_to prefix.

**Arguments**:

- `redirect_from`: str containing the prefix that should be redirected
- `redirect_to`: str containing the prefix that should be redirected to

**Raises**:

- `ValueError`: if the redirect destination does not exist in the namespace map or if the redirect source already exists in the namespace map

<a id="brel.qname.QNameNSMap.get_redirect"></a>

#### get\_redirect

```python
def get_redirect(redirect_from: str) -> str | None
```

Gets the redirect destination for a prefix redirect

**Arguments**:

- `redirect_from`: str containing the prefix that should be redirected

**Returns**:

`str`: containing the prefix that should be redirected to

<a id="brel.qname.QNameNSMap.rename"></a>

#### rename

```python
def rename(rename_uri: str, rename_prefix: str) -> None
```

Given a URI and a prefix, changes the mapping of the URI to the prefix.

When creating a new QName and only the URI is known, the prefix will be replaced with the rename_prefix.

**Arguments**:

- `rename_uri`: str containing the URI
- `rename_prefix`: str containing the prefix

**Raises**:

- `ValueError`: if the URI does not exist in the namespace map

<a id="brel.qname.QNameNSMap.get_prefix"></a>

#### get\_prefix

```python
def get_prefix(url: str) -> str | None
```

Gets the prefix for a URL

:param url: str containing the URL.
:return str | None: The prefix for the URL. None if the URL is not in the namespace map


<a id="brel.qname.QNameNSMap.get_url"></a>

#### get\_url

```python
def get_url(prefix: str) -> str | None
```

Gets the URL for a prefix

:param prefix: str containing the prefix
:return str | None: The URL for the prefix. None if the prefix is not in the namespace map


<a id="brel.qname.QNameNSMap.get_nsmap"></a>

#### get\_nsmap

```python
def get_nsmap() -> dict[str, str]
```

Returns the namespace map as a dict.

This is deprecated. Use QNameNSMap.get_prefix()
:return dict[str, str]: containing the namespace map


