from urllib.parse import urlparse


def is_valid_uri(uri: str) -> bool:
    """
    Checks whether the provided string is a valid URI (absolute or relative)
    :param uri: the string to check
    :return: True if the string is a valid URI, False otherwise.
    """
    try:
        result = urlparse(uri)
        return result.path != "" or result.scheme != "" and result.netloc != ""
    except Exception:
        return False
