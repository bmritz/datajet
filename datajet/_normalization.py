"""Functions to normailze a datajet map."""
from inspect import Parameter, signature
from itertools import chain


class IncompatableFunctionError(ValueError):
    pass


def _get_list_of_input_variables_from_function(f):
    """Return a list of input parameter names for the function `f`

    Raises:
        IncompatableFunctionError if a function has *args or **kwargs.

    """
    sig = signature(f)
    if any(
        param.kind in set([Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD, Parameter.KEYWORD_ONLY])
        for param in sig.parameters.values()
    ):
        raise IncompatableFunctionError(f"The function {f} must not have *args, **kwargs, or keyword-only arguments.")

    return list(sig.parameters)


def _norm(v) -> list:
    if callable(v):
        return [{"in": _get_list_of_input_variables_from_function(v), "f": v}]
    if isinstance(v, dict):
        return [{"in": v.get("in", _get_list_of_input_variables_from_function(v["f"])), "f": v["f"]}]
    if isinstance(v, list):
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
