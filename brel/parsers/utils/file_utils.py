"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 May 2025

====================
"""

import re


def uri_to_filename(uri: str) -> str:
    """
    Converts a uri to a filename.
    The filename is unique as long as the uri is unique.
    :param uri: the uri to convert
    :returns str: the filename
    """

    file_format_match = re.search(r"\.([a-zA-Z0-9]+)$", uri)
    file_format = "." + file_format_match.group(1) if file_format_match else ""

    if not uri.startswith("http"):
        if "/" in uri:
            return uri.split("/")[-1]
        else:
            return uri

    uri = uri.replace("." + file_format, "")

    if "http" in uri:
        # remove http and https
        uri = uri.replace("http://", "")
        uri = uri.replace("https://", "")

        # replace www. and things like .com, .org, etc.
        uri = uri.replace("www.", "")
        # the .com is between the first . and the first /
        # uri = uri.split(".")[0] + uri.split("/")[1]
    # replace all / with _
    uri = uri.replace("/", "_")
    # replace all : with _
    uri = uri.replace(":", "_")
    # replace all ? with _
    uri = uri.replace("?", "_")
    # replace all . with _
    uri = uri.replace(".", "_")
    # replace all \ with _
    uri = uri.replace("\\", "_")

    return uri + file_format
