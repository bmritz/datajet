"""Common resolvers that can be used as shortcuts in creating a datamap."""


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
