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


def dict_resolver(input_node: Hashable, d: dict) -> List[dict]:
    """Returns a resolver function that looks up the resulting value from `d` corresponding with the key output from the `input_node`.

    Notes:
        The resolver will raise RuntimeResolutionException if the key is not found in the dict at "resolution time."
    """

    def _f(key):
        try:
            return d[key]
        except KeyError:
            raise RuntimeResolutionException

    return [{"in": [input_node], "f": _f}]
