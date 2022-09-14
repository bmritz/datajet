"""Validation for datajet maps."""
import operator

from ._normalization import (
    _function_has_variadic_positional_argument,
    _get_list_of_input_variables_from_function,
)


def _data_map_value_is_list_or_tuple(data_map_value: list) -> bool:
    return isinstance(
        data_map_value,
        (
            list,
            tuple,
        ),
    )


def _data_map_value_dict_contains_key_f(data_map_value: dict) -> bool:
    return "f" in data_map_value


def _data_map_value_dict_is_dict(data_map_value: dict) -> bool:
    return isinstance(data_map_value, (dict,))


def _data_map_value_dict_has_expected_keys_and_expected_keys_only(data_map_value: dict) -> bool:
    expected_keys = set(("in", "f"))
    return len(set(data_map_value).symmetric_difference(expected_keys)) == 0


def _data_map_value_dict_key_f_is_callable(data_map_value: dict) -> bool:
    return callable(data_map_value["f"])


def _data_map_value_dict_key_f_has_correct_arity(data_map_value: dict) -> bool:
    arity = len(data_map_value.get("in", []))
    func = data_map_value["f"]
    function_args = _get_list_of_input_variables_from_function(func)
    if _function_has_variadic_positional_argument(func):
        op = operator.ge
    else:
        op = operator.eq
    return op(arity, len(function_args))


def _data_map_value_dict_key_in_is_list_or_tuple(data_map_value: dict) -> bool:
    return isinstance(data_map_value.get("in", []), (list, tuple))


def _data_map_dependencies_are_present(data_map: dict) -> bool:
    return all((el in data_map for ll in data_map.values() for v in ll for el in v.get("in", [])))


_data_map_value_dict_validation_check_functions = {
    # these are the functions that validate each dict inside a data_map_value
    _data_map_value_dict_is_dict: "is not a dict.",
    _data_map_value_dict_contains_key_f: "does not contain key f.",
    _data_map_value_dict_has_expected_keys_and_expected_keys_only: "does not contain keys 'in' and 'f' and only those keys.",
    _data_map_value_dict_key_f_is_callable: "does not contain value at key 'f' that is callable",
    _data_map_value_dict_key_in_is_list_or_tuple: "does not contain value at key 'in' that is a list or tuple.",
    _data_map_value_dict_key_f_has_correct_arity: "does not contain a function a key 'f' with expected arity.",
}


def _normalized_data_map_validation_error(data_map: dict) -> str:
    """Return a list of validation errors for `data_map`"""
    errors = []
    if not isinstance(data_map, dict):
        return "Data map is not a dict."

    for key, data_map_value in data_map.items():

        if not _data_map_value_is_list_or_tuple(data_map_value):
            return f"Data map value at key {key} is not a list or tuple"

        for possible_input in data_map_value:
            for check, error_message in _data_map_value_dict_validation_check_functions.items():
                if not check(possible_input):
                    return f"Data map input {possible_input} at key {key} " + error_message

    if not errors and not _data_map_dependencies_are_present(data_map):
        return "A data dependency in the data map is not present in the map."

    return ""


def _is_valid_normalized_data_map(data_map: dict) -> bool:
    return not bool(_normalized_data_map_validation_error(data_map))
