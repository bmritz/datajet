import pytest

from datajet.normalization import _norm


def assert_structure(ll):
    assert isinstance(ll, list)
    for d in ll:
        assert isinstance(d, (dict,))
        assert "f" in d
        assert "in" in d


def test_norm_for_constant_list_gives_unexpected_result():
    v = [1, 2, 3, 4]
    r = _norm(v)
    assert_structure(r)
    assert len(r) == 4
    assert all([r[i]["f"]() == j for i, j in zip(range(4), v)])


@pytest.mark.parametrize("f", [None, lambda x: [x]])
def test_norm_for_singleton(f):
    v = 1
    if f is not None:
        v = f(v)
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
