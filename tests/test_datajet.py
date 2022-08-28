import pytest

from datajet.data_map_helpers import _get_dependencies


@pytest.mark.parametrize(
    "data_map,key,expected_result",
    [
        ({"a": {"f": lambda: 1}}, "a", [["a"]]),
        ({"a": {"in": ["b"], "f": lambda x: 1 + x}, "b": {"f": lambda: 2}}, "a", [["a", "b"]]),
        (
            {"a": {"in": ["b"], "f": lambda x: 1}, "b": {"in": ["c"], "f": lambda x: 1}, "c": {"f": lambda: 1}},
            "a",
            [["a", "b", "c"]],
        ),
        (
            {"a": {"in": ["b"], "f": lambda x: 1}, "b": {"in": ["c"], "f": lambda x: 1}, "c": {"f": lambda: 1}},
            "b",
            [["b", "c"]],
        ),
        (
            {"a": {"in": ["b", "c"], "f": lambda x, y: 1}, "b": {"in": ["c"], "f": lambda x: 1}, "c": {"f": lambda: 1}},
            "a",
            [["a", "b", "c"]],
        ),
    ],
)
def test_get_dependencies(data_map, key, expected_result):
    assert _get_dependencies(data_map, key) == expected_result
