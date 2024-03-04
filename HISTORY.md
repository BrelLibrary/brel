Changelog
=========


# 0.1.2 (2021-08-14)
- Fix release, README and windows CI. [Bruno Rocha]
- Release: version 0.1.0. [Bruno Rocha]


# 0.1.0 (2021-08-14)
- Add release command. [Bruno Rocha]

# 0.8.1.aq (2024-02-26)
- Added support for opening filings via URIs.
- Added helper for EDGAR filings.
- Reworked file cache
- Added more test cases
- Fixed network parsing issues
- Fixed bug that didn't allow empty resources
- Improved performance of network parsing
- Cleaned up documentation
- Cleaned up code

# Version 0.8.1.a0 (2024-01-11)

Initial release of Brel. This release includes the following features:

- Loading an XBRL file from a local path.
- Support for XML XBRL format.
- Implementation of Brel API, a pythonic wrapper for XBRL
- Support for filings from the SEC's EDGAR database.

# Version 0.8.1.a1 (2024-02-28)

This release includes the following features:

- Support for the `open_edgar` function to load filings from the SEC's EDGAR database.
- Support for remote file loading from the SEC's EDGAR database.
- Improved performance of the `Filing.open` method.
- Added the `Filing.get_errors` method. Errors in the filing are now logged instead of raising an exception.

Bugfixes:

- Fixed an issue where empty footnotes would raise an exception.
- Fixed an issue where calculation network weights were not being extracted correctly.
- Removed typos in two methods.
- Fixed renaming of namespaces normalization not working correctly.
- Patched bug where schemaLocations were not discovered by DTS resolver.
- Fixed pprint functions not properly displaying footnotes and references correctly.

Internal changes:

- Removed all `from_xml` methods and moved them into parser modules.
- Added more dependency injection to the parser. Now QNames, namespaces, etc. are created using first order functions.
- `Filing.open` is now strict with the input parameters.
- Removed lots of TODOs
- Added tons and tons of documentation.
- Added a lot of tests. Test coverage is now at 87%.

# Version 0.8.1.a2 (2024-02-28)

Bugfixes:

- Fixed linting issues.
- Fixed pointers to the github pages documentation.
- Added this changelog as a markdown file.
- Updated the documentation to reflect the new changes that were missing.

# Version 0.8.1.a3 (2024-03-04)

Bugfixes:

- Fixed a critical bug for windows where a file of the report might be loaded multiple times, resulting in duplicate elements.
- Made all paths in the code OS-agnostic.
- Updated the documentation to reflect the new changes that were missing.
- Updated the test cases to reflect the new changes that were missing.
