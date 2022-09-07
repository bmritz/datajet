"""Exceptions for the `datajet` module."""


class RuntimeResolutionException(Exception):
    """A exception was raised during execution of the datamap for fields."""


class PlanNotFoundError(ValueError):
    """A valid plan was not found in the datamap."""
