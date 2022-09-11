"""Exceptions for the `datajet` module."""


class RuntimeResolutionException(Exception):
    """A exception was raised during execution of the datamap for fields."""


class PlanNotFoundError(ValueError):
    """A valid plan was not found in the datamap."""


class IncompatableFunctionError(ValueError):
    """The function signature cannot be expressed in the current datamap schema."""

    pass
