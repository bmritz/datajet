"""Exceptions for the `datajet` module."""


class RuntimeResolutionException(Exception):
    """A exception was raised during execution of the datamap for fields.

    Usage:
        Raise this exception inside a resolver to indicate to datajet that the resolution
        of the resolver is not possible with the given inputs. DataJet will catch and ignore this exception
        and proceed with other valid execution paths that return the requested fields in the DataMap if they exist.

    """


class PlanNotFoundError(ValueError):
    """A valid plan was not found in the datamap to return the fields requested.

    Notes:
        This is typically raised by DataJet when it is no viable paths (paths that do not raise `RuntimeResolutionException`)
        exist in the datamap to return the requested fields.
    """


class IncompatableFunctionError(ValueError):
    """The function signature cannot be expressed in the current datamap schema."""
