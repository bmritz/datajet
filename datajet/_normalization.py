"""Functions to normailze a datajet map."""
from inspect import Parameter, signature
from itertools import chain
from typing import Callable, List

from .common_resolvers import _REQUIRED_FROM_CONTEXT
from .exceptions import IncompatableFunctionError


def _function_has_variadic_positional_argument(f):
    """Return `True` if the function has a variadic positional argument in it's signature, else `False`"""
    sig = signature(f)
    return any(param.kind == Parameter.VAR_POSITIONAL for param in sig.parameters.values())


def _get_list_of_input_variables_from_function(f: Callable) -> List[Parameter]:
    """Return a list of input parameter names for the function `f`

    Raises:
        IncompatableFunctionError if a function has *args or **kwargs.

    """
    sig = signature(f)
    accum = []
    for param in sig.parameters.values():
        if param.kind in set([Parameter.VAR_KEYWORD, Parameter.KEYWORD_ONLY]):
            raise IncompatableFunctionError(
                f"The function {f} must not have *args, **kwargs, or keyword-only arguments."
            )
        accum.append(param)
    return accum


def _norm(v) -> list:
    """Normalize a data map value."""
    if callable(v):
        return [{"in": [p.name for p in _get_list_of_input_variables_from_function(v)], "f": v}]
    if isinstance(v, dict):
        # if the dict has key "f", assume it is a resolver
        try:
            f = v["f"]
        except KeyError:
            return [{"in": [], "f": lambda: v}]
        else:
            if callable(f):
                return [{"in": v.get("in", [p.name for p in _get_list_of_input_variables_from_function(f)]), "f": f}]
            return [{"in": [], "f": lambda: v}]
    if isinstance(v, list):
        if v == []:
            return _REQUIRED_FROM_CONTEXT
        accum = []
        for el in v:
            is_callable = callable(el)
            is_dict_with_key_f = isinstance(el, dict) and "f" in el
            if not is_callable and not is_dict_with_key_f:
                accum.append(False)
            else:
                accum.append(True)
        if all(accum):
            return list(chain.from_iterable(_norm(el) for el in v))
        elif all(not el for el in accum):
            pass  # go to the final line of the function and return the value in a bare lambda
        else:
            raise ValueError("The data map value {} is not valid.".format(v))
    return [{"in": [], "f": lambda: v}]


def _normalize_data_map(data_map: dict) -> dict:
    return {k: _norm(v) for k, v in data_map.items()}
