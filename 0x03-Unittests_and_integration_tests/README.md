# Python Unit Testing: Access Nested Map

This project focuses on writing proper unit tests in Python using the `unittest` module. It covers key testing patterns such as parameterization and mocking, while reinforcing the concepts of unit and integration testing.

## Objectives

- Understand the difference between unit and integration tests
- Write parameterized unit tests
- Use fixtures and mocking in test cases
- Document modules, classes, and methods correctly
- Apply type annotations in all functions and methods

## What Was Tested

The main function tested is:

### `utils.access_nested_map(nested_map, path)`

This function takes a dictionary and a path (tuple of keys) and returns the value at the end of the path. For example:

```python
access_nested_map({"a": {"b": 2}}, ("a", "b"))  # returns 2
