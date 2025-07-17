#!/usr/bin/env python3
"""
This module provides utility functions for accessing nested data structures.
"""


from typing import Any, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested dictionary using a sequence of keys.

    Args:
        nested_map (dict): A dictionary that may contain nested dictionaries.
        path (tuple): A sequence of keys to navigate through the nested map.

    Returns:
        The value at the end of the path.

    Raises:
        KeyError: If a key in the path is not found.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map
