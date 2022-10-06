"""Common resolvers that can be used as shortcuts in creating a datamap."""


from typing import Hashable, List

from .exceptions import RuntimeResolutionException


def _raise():
    raise RuntimeResolutionException


_REQUIRED_FROM_CONTEXT = [{"in": [], "f": _raise}]


def required_from_context():
    """Returns a resolver function that anticipates and requires input from the context.

    Use this as a "placeholder" in your datamap for context.

    Notes:
        Prefer to use this function over raising a `RuntimeResolutionException`, as
        the engine that powers `datajet.execute` will optimize the search for
        a valid data-path (to increase performance) if a `context_input` is not given in the context.

    """

    return _REQUIRED_FROM_CONTEXT


def dict_resolver(input_datapoint: Hashable, d: dict) -> List[dict]:
    """Returns a resolver function that looks up the resulting value from `d` corresponding with the key output from `input_datapoint`.

    Args:
        input_node: The datapoint that will be looked up in `d` to find the value returned from this resolver.
        d: The dict to lookup `input_datapoint` in.

    Notes:
        The resolver will raise RuntimeResolutionException if the key is not found in the dict at "resolution time."
    """

    def _f(key):
        try:
            return d[key]
        except KeyError:
            raise RuntimeResolutionException

    return [{"in": [input_datapoint], "f": _f}]


def alias(datapoint: Hashable) -> List[dict]:
    """Returns a resolver function that acts as an alias to the `node`.

    Args:
        datapoint: The datapoint to alias.

    Notes:
        Use the resolver output from this function to pass through the data from one node directly to another.

    """
    return [{"in": [datapoint], "f": lambda x: x}]
