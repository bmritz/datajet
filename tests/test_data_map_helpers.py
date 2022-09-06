import pytest

from datajet.data_map_helpers import (
    PlanNotFoundError,
    _get_dependencies_for_key,
    _get_dependencies_from_normalized_datamap,
    _unique_everseen,
    _unique_everseen_reversed,
)

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
    "c": [{"in": ["a"], "f": lambda: 2}],
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


# datamap_11 = {
#     "a": [{"in": ["b"], "f": lambda x: x + 1}],
#     "b": [{"in": ["c"], "f": lambda x: x + 1}],
#     "c": [{"in": ["d"], "f": lambda x: x + 1}, {"in": ["h"], "f": lambda x: x + 1}],
#     "d": [{"in": ["e"], "f": lambda x: x + 1}],
#     "e": [{"in": ["c"], "f": lambda x: x - 10}, {"in": ["f"], "f": lambda x: x + 1}],
#     "f": [{"in": ["g"], "f": lambda x: x + 1}],
#     "g": [{"in": [], "f": lambda: 1}],
#     "h": [{"in": [], "f": lambda: 1}],
# }

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
    "it,key,expected", [("AAAABBBCCDAABBB", None, ["C", "D", "A", "B"]), ("ABBCcAD", str.lower, ["B", "c", "A", "D"])]
)
def test_unique_everseen_reversed(it, key, expected):
    assert list(_unique_everseen_reversed(it, key)) == expected


@pytest.mark.parametrize(
    "datamap,key,expected",
    [
        (datamap_1, "a", [["a", "b", "e", "d"], ["a", "b", "e", "c"], ["a", "c"]]),
        (datamap_1, "c", [["c"]]),
        (datamap_1, "b", [["b", "d"], ["b", "c"]]),
        (
            datamap_2,
            "a",
            [
                ["a", "b", "c", "d", "e", "i", "g", "h"],
                ["a", "b", "c", "d", "e", "j", "g", "h"],
                ["a", "b", "c", "f", "g", "h"],
                ["a", "c", "d", "g", "h", "i"],
                ["a", "c", "d", "g", "h", "j"],
            ],
        ),
        (datamap_2, "b", [["b", "d", "e", "i"], ["b", "d", "e", "j"], ["b", "f"]]),
        (datamap_2, "c", [["c", "g", "h"]]),
        (datamap_3, "a", [["a", "b", "c"]]),
        (datamap_4, "a", [["a", "b", "c"]]),
        (datamap_6, "a", [["a", "d", "e"]]),
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
    ],
)
def test_get_dependencies_from_normalized_datamap(datamap, key, expected):
    assert _get_dependencies_from_normalized_datamap(datamap, key) == expected


@pytest.mark.parametrize(
    "datamap,key,expected",
    [
        (datamap_5, "a", []),
        (datamap_8, "a", []),
    ],
)
def test_get_dependencies_from_normalized_datamap_raises(datamap, key, expected):
    with pytest.raises(PlanNotFoundError):
        _get_dependencies_from_normalized_datamap(datamap, key) == expected
