import pytest

from datajet._validations import _is_valid_normalized_data_map

invalid_datamaps = [
    {"b": 1},
    {"b": lambda: 1},
    {"b": [lambda: 1]},
    # extra key
    {"b": [{"in": [], "f": lambda x: 1, "extra": [1, 2]}]},
    # missing key
    {"a": [{"f": lambda: 1}]},
    # dependency not met
    {"a": [{"in": ["b"], "f": lambda x: 1}]},
    # function for "a" is wrong arity
    {"a": [{"in": ["b"], "f": lambda: 1}], "b": [{"in": [], "f": lambda: 1}]},
]

valid_datamaps = [
    {"b": [{"in": [], "f": lambda: 1}]},
    {"a": [{"in": ["b"], "f": lambda x: 1}], "b": [{"in": [], "f": lambda: 1}]},
    {
        "a": [{"in": ["b"], "f": lambda x: 1}],
        "b": [
            {"in": [], "f": lambda: 1},
            {"in": ["c"], "f": lambda x: x + 1},
        ],
        "c": [{"in": [], "f": lambda: 3}],
    },
]


@pytest.mark.parametrize("datamap", invalid_datamaps)
def test_is_valid_normalized_data_map_returns_false_on_invalid_datamap(datamap):
    assert not _is_valid_normalized_data_map(datamap)


@pytest.mark.parametrize("datamap", valid_datamaps)
def test_is_valid_normalized_data_map_returns_true_on_valid_datamap(datamap):
    assert _is_valid_normalized_data_map(datamap)
