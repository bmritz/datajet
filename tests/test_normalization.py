import pytest

from datajet._normalization import (
    _function_has_variadic_positional_argument,
    _get_list_of_input_variables_from_function,
    _norm,
    _normalize_data_map,
)
from datajet.common_resolvers import _raise
from datajet.exceptions import IncompatableFunctionError


def dummy_function_1(x, y):
    z = x + y
    a = z + 4
    return a


def dummy_function_2():
    z = 2
    z = z * z
    return z


def dummy_function_3(*args):
    return 1


def dummy_function_4(x, y, *args):
    return 1


def dummy_function_fail_3(*args, **kwargs):
    return 1


def dummy_function_fail_4(x, *args, **kwargs):
    return 1


def dummy_function_fail_5(x, **kwargs):
    return 1


def dummy_function_fail_6(**kwargs):
    return 1


def dummy_function_fail_7(x, y, *, z):
    return 1


def assert_structure(ll):
    assert isinstance(ll, list)
    for d in ll:
        assert isinstance(d, (dict,))
        assert "f" in d
        assert "in" in d


def test_norm_for_constant_list():
    v = [1, 2, 3, 4]
    r = _norm(v)
    assert_structure(r)
    assert r[0]["f"]() == v


def test_norm_for_list_of_lambdas():
    v = [lambda a: 1, lambda b: 2]
    r = _norm(v)
    assert_structure(r)
    assert len(r) == 2
    assert [d["in"] for d in r] == [["a"], ["b"]]
    # 4 is just a dummy parameter here
    assert r[0]["f"](4) == 1
    assert r[1]["f"](4) == 2


def test_norm_for_bare_function_list():
    v = [dummy_function_1, dummy_function_2, lambda z: 2]
    r = _norm(v)
    assert_structure(r)
    assert len(r) == 3
    assert [d["in"] for d in r] == [["x", "y"], [], ["z"]]
    assert r[0]["f"](2, 2) == 8
    assert r[1]["f"]() == 4
    assert r[2]["f"](4) == 2


@pytest.mark.parametrize(
    "v",
    [
        [lambda a: 1, 2],
        [lambda: 2, {"f": lambda: 3}, "constant_string"],
        [{"f": lambda: 3}, "constant_string"],
    ],
)
def test_norm_for_list_of_mixed_constants_with_fxns_or_dicts_raises(v):
    v = [lambda a: 1, 2]
    with pytest.raises(ValueError):
        _norm(v)


def test_norm_for_singleton():
    v = 1
    r = _norm(v)
    assert_structure(r)
    assert r[0]["f"]() == 1


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_bare_lambda(f):
    v = lambda: 1
    if f is not None:
        v = f(v)
    r = _norm(v)
    assert_structure(r)
    assert r[0]["f"]() == 1


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_bare_function(f):
    v = dummy_function_2
    if f is not None:
        v = f(v)
    r = _norm(v)
    assert_structure(r)
    assert [d["in"] for d in r] == [[]]
    assert len(r) == 1
    assert r[0]["f"]() == 4


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_lambda_1_arg(f):
    v = lambda x: x + 1
    if f is not None:
        v = f(v)
    r = _norm(v)
    assert_structure(r)
    assert r[0]["in"] == ["x"]
    assert r[0]["f"](2) == 3


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_lambda_2_args(f):
    v = lambda x, y: x + y + 1
    if f is not None:
        v = f(v)
    r = _norm(v)
    assert_structure(r)
    assert r[0]["in"] == ["x", "y"]
    assert r[0]["f"](2, 5) == 8


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_lambda_2_args_w_f_key(f):
    v = {"f": lambda x, y: x + y + 1}
    if f is not None:
        v = f(v)
    r = _norm(v)
    assert_structure(r)
    assert r[0]["in"] == ["x", "y"]
    assert r[0]["f"](2, 5) == 8


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_lambda_2_args_w_f_key_and_in_key(f):
    v = {"in": ["this", "that"], "f": lambda x, y: x + y + 1}
    if f is not None:
        v = f(v)
    r = _norm(v)
    assert_structure(r)
    assert r[0]["in"] == ["this", "that"]
    assert r[0]["f"](2, 5) == 8


@pytest.mark.parametrize(
    "f,expected",
    [
        (lambda x: 1, False),
        (lambda: 1, False),
        (dummy_function_1, False),
        (dummy_function_2, False),
        (lambda *args: 1, True),
        (lambda x, *args: 1, True),
        (dummy_function_3, True),
        (dummy_function_4, True),
    ],
)
def test__function_has_variadic_positional_argument(f, expected):
    assert _function_has_variadic_positional_argument(f) == expected


@pytest.mark.parametrize(
    "f,expected",
    [
        (lambda x: 1, ["x"]),
        (lambda x, y: 1 + x + y, ["x", "y"]),
        (dummy_function_1, ["x", "y"]),
        (dummy_function_2, []),
        (lambda: 2, []),
        (lambda x, *args: 2, ["x"]),
        (lambda x, y, *args: 2, ["x", "y"]),
        (lambda *args: 2, []),
        (dummy_function_3, []),
        (dummy_function_4, ["x", "y"]),
    ],
)
def test_get_list_of_input_variables_from_function(f, expected):
    assert _get_list_of_input_variables_from_function(f) == expected


@pytest.mark.parametrize(
    "f",
    [
        dummy_function_fail_3,
        dummy_function_fail_4,
        dummy_function_fail_5,
        dummy_function_fail_6,
        dummy_function_fail_7,
        lambda **kwargs: 1,
        lambda x, **kargs: 1,
        lambda x, *args, **kwargs: 1,
        lambda x, y, *, z: 1,
    ],
)
def test_get_list_of_input_variables_from_function_fails(f):
    with pytest.raises(IncompatableFunctionError):
        assert _get_list_of_input_variables_from_function(f)


def test_key_with_empty_list_is_replaced_with_function_that_raises():
    fa = lambda a: a + 1
    fb = lambda c: c + 2
    fc = lambda: 2
    datamap = {"a": [], "b": [fa, fb], "c": fc}

    assert _normalize_data_map(datamap) == {
        "a": [{"in": [], "f": _raise}],
        "b": [{"in": ["a"], "f": fa}, {"in": ["c"], "f": fb}],
        "c": [{"in": [], "f": fc}],
    }
