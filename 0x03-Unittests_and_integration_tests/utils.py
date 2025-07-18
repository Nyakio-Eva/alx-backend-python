#!/usr/bin/env python3
"""
This module provides utility functions for accessing nested data structures.
"""
import requests
from typing import Dict
from functools import wraps
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

"""
Utility module for making HTTP requests.
"""

def get_json(url: str) -> Dict:
    """
    Fetches and returns the JSON content from a given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: Parsed JSON content from the response.
    """
    response = requests.get(url)
    return response.json()

"""
Utility module for caching with memoization.
"""

def memoize(method):
    """
    Decorator to cache method results per instance.
    """
    attr_name = "_{}".format(method.__name__)

    @property
    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper

