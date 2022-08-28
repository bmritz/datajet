import pytest

from datajet.normalization import _norm


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
    # 4 is just a dummy parameter here
    assert r[0]["f"](4) == 1
    assert r[1]["f"](4) == 2


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
