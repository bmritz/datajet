"""Validation for datajet maps."""


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


def _data_map_valid_dict_is_dict(data_map_value: dict) -> bool:
    return isinstance(data_map_value, (dict,))


def _data_map_value_dict_has_expected_keys_and_expected_keys_only(data_map_value: dict) -> bool:
    expected_keys = set(("in", "f"))
    return len(set(data_map_value).symmetric_difference(expected_keys)) == 0


def _data_map_value_dict_key_f_is_callable(data_map_value: dict) -> bool:
    return callable(data_map_value["f"])


def _data_map_value_dict_key_f_has_correct_arity(data_map_value: dict) -> bool:
    arity = len(data_map_value.get("in", []))
    func = data_map_value["f"]
    return len(list(func.__code__.co_varnames)) == arity


def _data_map_value_dict_key_in_is_list_or_tuple(data_map_value: dict) -> bool:
    return isinstance(data_map_value.get("in", []), (list, tuple))


def _data_map_dependencies_are_present(data_map: dict) -> bool:
    return all((el in data_map for ll in data_map.values() for v in ll for el in v.get("in", [])))


def _is_valid_normalized_data_map(data_map: dict) -> bool:

    data_map_value_dict_validation_check_functions = [
        # these are the functions that validate each dict inside a data_map_value
        _data_map_valid_dict_is_dict,
        _data_map_value_dict_contains_key_f,
        _data_map_value_dict_has_expected_keys_and_expected_keys_only,
        _data_map_value_dict_key_f_is_callable,
        _data_map_value_dict_key_in_is_list_or_tuple,
        _data_map_value_dict_key_f_has_correct_arity,
    ]

    does_value_pass_all_checks = lambda data_map_value: (
        _data_map_value_is_list_or_tuple(data_map_value)
        and all(
            (
                f(data_map_value_dict)
                for f in data_map_value_dict_validation_check_functions
                for data_map_value_dict in data_map_value
            )
        )
    )

    value_checks_pass = map(does_value_pass_all_checks, data_map.values())
    return all(value_checks_pass) and _data_map_dependencies_are_present(data_map)
