import pytest

from datajet import DataJetMap, execute
from datajet._data_map_helpers import _get_dependencies
from datajet.exceptions import RuntimeResolutionException


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
    assert list(_get_dependencies(data_map, key)) == expected_result


@pytest.mark.parametrize(
    "data_map,fields,expected_result",
    [
        (
            {
                "dollars": [
                    3.99,
                    10.47,
                    18.95,
                    15.16,
                ],
                "units": [
                    1,
                    3,
                    5,
                    4,
                ],
                "prices": lambda dollars, units: [d / u for d, u in zip(dollars, units)],
                "average_price": lambda prices: sum(prices) / len(prices) * 1000 // 10 / 100,
            },
            ["prices", "average_price"],
            {"prices": [3.99, 3.49, 3.79, 3.79], "average_price": 3.76},
        ),
        ({"a": lambda: 1, "b": lambda a: a + 3, "c": lambda a: a + 2, "d": lambda b, c: b * c}, ["d"], {"d": 12}),
    ],
)
def test_execute(data_map, fields, expected_result):
    assert execute(data_map, fields) == expected_result


def test_execute_closes_off_path_with_manual_execution_raise():
    def raises(x):
        if x > 1:
            raise RuntimeResolutionException
        else:
            return x + 2

    data_map = {
        "a": lambda: 2,
        "b1": [{"in": ["a"], "f": raises}],
        "b2": lambda a: a + 2,
        "b": [lambda b1: b1 + 20, lambda b2: b2 + 2],
    }
    assert execute(data_map, "b") == {"b": 6}
    assert execute(data_map, "b", context={"a": lambda: 1}) == {"b": 23}


def test_execute_raises_when_path_must_go_through_runtime_exception():
    def raises(x):
        raise RuntimeResolutionException

    data_map = {
        "a": lambda: 2,
        "b1": [{"in": ["a"], "f": raises}],
        "b": [lambda b1: b1 + 2],
    }
    with pytest.raises(RuntimeResolutionException):
        execute(data_map, "b") == {"b": 6}


def test_execute_works_with_datajet_map():

    data_map = DataJetMap()

    @data_map.register()
    def a():
        return 2

    @data_map.register()
    def b():
        return 6

    @data_map.register()
    def c(a, b):
        return a + b

    execute(data_map, fields=["a", "b", "c"]) == {"a": 2, "b": 6, "c": 8}
