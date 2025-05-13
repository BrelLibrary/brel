"""
====================

- author: Robin Schmidiger
- version: 0.1
- date: 12 May 2025

====================
"""


def get_or_raise[T](value: T | None, error_message: Exception | None = None) -> T:
    if value is None:
        if error_message is None:
            raise ValueError("Value cannot be None")
        else:
            raise error_message
    return value
