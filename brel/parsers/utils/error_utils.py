"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 13 April 2025

====================
"""


def error_on_none[
    T
](value: T | None, error_message: str,) -> T:
    """
    Raise a ValueError if the value is None.
    :param value: The value to check.
    :param error_message: The error message to raise if the value is None.
    :raises ValueError: If the value is None.
    """
    if value is None:
        raise ValueError(error_message)
    return value
