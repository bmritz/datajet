"""Functions to normailze a datajet map."""
from itertools import chain


def _norm(v) -> list:
    if callable(v):
        return [{"in": list(v.__code__.co_varnames), "f": v}]
    if isinstance(v, dict):
        return [{"in": v.get("in", list(v["f"].__code__.co_varnames)), "f": v["f"]}]
    if isinstance(v, list):
        return list(chain.from_iterable(_norm(el) for el in v))
    return [{"in": [], "f": lambda: v}]


def _normalize_data_map(data_map: dict) -> dict:
    return {k: _norm(v) for k, v in data_map.items()}
