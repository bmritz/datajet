import pytest

from datajet._data_map_helpers import (
    _get_dependencies,
    _get_dependencies_for_key,
    _get_dependencies_from_normalized_datamap,
    _unique_everseen,
)
from datajet.common_resolvers import _REQUIRED_FROM_CONTEXT, required_from_context
from datajet.exceptions import PlanNotFoundError

datamap_1 = {
    "a": [{"in": ["b", "e"], "f": lambda x, y: 1}, {"in": ["c"], "f": lambda x: 1}],
    "b": [{"in": ["d"], "f": lambda x: 1}, {"in": ["c"], "f": lambda x: 1}],
    "c": [{"in": [], "f": lambda: 1}],
    "d": [{"in": [], "f": lambda: 1}],
    "e": [{"in": [], "f": lambda: 1}],
}

datamap_2 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: 1}, {"in": ["c", "d"], "f": lambda x: 1}],
    "b": [{"in": ["d", "e"], "f": lambda x, y: 1}, {"in": ["f"], "f": lambda x: 1}],
    "c": [{"in": ["g", "h"], "f": lambda x, y: 1}],
    "d": [{"in": ["i"], "f": lambda x: 1}, {"in": ["j"], "f": lambda x: 1}],
    "e": [{"in": [], "f": lambda: 1}],
    "f": [{"in": [], "f": lambda: 1}],
    "g": [{"in": [], "f": lambda: 1}],
    "h": [{"in": [], "f": lambda: 1}],
    "i": [{"in": [], "f": lambda: 1}],
    "j": [{"in": [], "f": lambda: 1}],
}

datamap_3 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: 1}],
    "b": [{"in": [], "f": lambda: 1}],
    "c": [{"in": [], "f": lambda: 1}],
}

datamap_4 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: 3}],
    "b": [{"in": ["c"], "f": lambda x: 2}],
    "c": [{"in": [], "f": lambda: 2}],
}


# test for circularity
datamap_5 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: 3}],
    "b": [{"in": ["c"], "f": lambda x: 2}],
    "c": [{"in": ["a"], "f": lambda x: 2}],
}

# test that a non-circular path is found in presence of circular path
datamap_6 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: 3}, {"in": ["d", "e"], "f": lambda x, y: 3}],
    "b": [{"in": ["c"], "f": lambda x: 2}],
    "c": [{"in": ["a"], "f": lambda x: 2}],
    "d": [{"in": [], "f": lambda: 2}],
    "e": [{"in": [], "f": lambda: 2}],
}

datamap_7 = {
    "a": [{"in": [], "f": lambda: 3}],
}

# test for circularity on two paths
datamap_8 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: x + y}, {"in": ["d"], "f": lambda y: 3}],
    "b": [{"in": ["c"], "f": lambda x: 2}],
    "c": [{"in": ["a"], "f": lambda x: 2}],
    "d": [{"in": ["b"], "f": lambda x: 2}],
}

datamap_9 = {
    "category": [{"in": ["category_tag"], "f": lambda x: {"Y": "X"}.get(x)}],
    "category_tag": [
        {"in": ["category"], "f": lambda x: {"x": "y"}.get(x)},
        {"in": ["subcategory"], "f": lambda x: {"Z": "Y"}.get(x)},
    ],
    "subcategory": [{"in": ["subcategory_tag"], "f": lambda x: {"NPF": "Z"}.get(x)}],
    "department_tag": [{"in": ["category"], "f": lambda x: {"X": "W"}.get(x)}],
    "department": [{"in": ["department_tag"], "f": lambda x: {"W": "V"}.get(x)}],
    "subcategory_tag": [{"in": [], "f": lambda: "NPF"}],
}

datamap_10 = {
    "a": [{"in": [], "f": lambda: 1}],
    "b": [{"in": ["a"], "f": lambda a: a + 3}],
    "c": [{"in": ["a"], "f": lambda a: a + 2}],
    "d": [{"in": ["b", "c"], "f": lambda b, c: b * c}],
}

datamap_11 = {
    "a": [{"in": ["b"], "f": lambda x: x + 1}],
    "b": [{"in": ["c"], "f": lambda x: x + 1}, {"in": ["d"], "f": lambda x: x + 1}],
    "c": _REQUIRED_FROM_CONTEXT,
    "d": [{"in": [], "f": lambda: 10}],
}

datamap_12 = {
    "b": [{"in": [], "f": lambda: 1}],
    "c": [{"in": [], "f": lambda: 1}],
    "a": [{"in": ["g", "c"], "f": lambda x, y: x + y + 1}],
    "j": [{"in": ["d", "k"], "f": lambda x, y: x + y + 1}, {"in": ["g", "h"], "f": lambda x, y: x + y + 1}],
    "h": [
        {"in": ["k", "a"], "f": lambda x, y: x + y + 1},
        {"in": ["k", "j"], "f": lambda x, y: x + y + 1},
        {"in": ["i", "m"], "f": lambda x, y: x + y + 1},
        {"in": ["i", "f"], "f": lambda x, y: x + y + 1},
    ],
    "g": [{"in": ["b"], "f": lambda x: x + 1}],
    "k": [{"in": ["b"], "f": lambda x: x + 1}],
    "e": [{"in": ["b"], "f": lambda x: x + 1}],
    "i": [{"in": ["b"], "f": lambda x: x + 1}],
    "m": [{"in": ["e", "c"], "f": lambda x, y: x + y + 1}],
    "f": [{"in": ["e", "h"], "f": lambda x, y: x + y + 1}, {"in": ["i", "l"], "f": lambda x, y: x + y + 1}],
    "l": [{"in": ["f"], "f": lambda x: x + 1}],
    "d": [{"in": [], "f": lambda: 1}],
}

datamap_13 = {
    "a": [{"in": ["b"], "f": lambda x: x + 1}],
    "b": [
        {"in": ["c"], "f": lambda x: x + 1},
    ],
    "c": _REQUIRED_FROM_CONTEXT,
}


@pytest.mark.parametrize(
    "datamap,key,expected",
    [
        (datamap_1, "a", [["b", "e"], ["c"]]),
        (datamap_1, "b", [["d"], ["c"]]),
        (datamap_1, "c", [[]]),
        # todo: add a few more tests for edge cases and tuple
    ],
)
def test_get_dependencies_for_key(datamap, key, expected):
    assert list(_get_dependencies_for_key(datamap, key)) == expected


@pytest.mark.parametrize(
    "it,key,expected", [("AAAABBBCCDAABBB", None, ["A", "B", "C", "D"]), ("ABBCcAD", str.lower, ["A", "B", "C", "D"])]
)
def test_unique_everseen(it, key, expected):
    assert list(_unique_everseen(it, key)) == expected


@pytest.mark.parametrize(
    "datamap,key,expected",
    [
        (datamap_1, "a", [["a", "e", "b", "d"], ["a", "e", "b", "c"], ["a", "c"]]),
        (datamap_1, "c", [["c"]]),
        (datamap_1, "b", [["b", "d"], ["b", "c"]]),
        (
            datamap_2,
            "a",
            [
                ["a", "c", "h", "g", "b", "e", "d", "i"],
                ["a", "c", "h", "g", "b", "e", "d", "j"],
                ["a", "c", "h", "g", "b", "f"],
                ["a", "d", "i", "c", "h", "g"],
                ["a", "d", "j", "c", "h", "g"],
            ],
        ),
        (datamap_2, "b", [["b", "e", "d", "i"], ["b", "e", "d", "j"], ["b", "f"]]),
        (datamap_2, "c", [["c", "h", "g"]]),
        (datamap_3, "a", [["a", "c", "b"]]),
        (datamap_4, "a", [["a", "b", "c"]]),
        (datamap_6, "a", [["a", "e", "d"]]),
        (datamap_7, "a", [["a"]]),
        (
            datamap_9,
            "department_tag",
            [["department_tag", "category", "category_tag", "subcategory", "subcategory_tag"]],
        ),
        (datamap_10, "d", [["d", "c", "b", "a"]]),
        (
            datamap_12,
            "f",
            [
                ["f", "h", "a", "c", "g", "k", "e", "b"],
                ["f", "h", "j", "d", "k", "e", "b"],
                ["f", "h", "m", "c", "i", "e", "b"],
            ],
        ),
        (datamap_5, "a", [None]),
        (datamap_8, "a", [None]),
        (datamap_11, "a", [["a", "b", "d"]]),
        ({**datamap_11, **{"c": required_from_context()}}, "a", [["a", "b", "d"]]),
    ],
)
def test_get_dependencies_from_normalized_datamap(datamap, key, expected):
    assert _get_dependencies_from_normalized_datamap(datamap, key) == expected


@pytest.mark.parametrize(
    "datamap,key",
    [(datamap_5, "a"), (datamap_8, "a"), (datamap_13, "a"), ({**datamap_13, **{"c": required_from_context()}}, "a")],
)
def test_get_dependencies_raises(datamap, key):
    with pytest.raises(PlanNotFoundError):
        _get_dependencies(datamap, key)
