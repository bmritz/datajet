import copy
from itertools import chain, filterfalse, product
from typing import Hashable, Iterable, List

from ._normalization import _normalize_data_map
from ._validations import (
    _is_valid_normalized_data_map,
    _normalized_data_map_validation_error,
)
from .common_resolvers import _REQUIRED_FROM_CONTEXT
from .exceptions import PlanNotFoundError


class KeyIsDeadEndException(Exception):
    pass


def _key_is_required_from_context(datamap: dict, key: Hashable) -> bool:
    return datamap[key] == _REQUIRED_FROM_CONTEXT


def _get_dependencies_for_key(datamap: dict, key: Hashable) -> Iterable[List[Hashable]]:
    """Return a list of the different potential 'paths' to a `key` in `datamap`.

    Parameters:
        datamap: A "normalized" dict that represents the data depdendencies.
        key: The key in the datamap dict to get the dependencies for.

    """
    yield from (list(d["in"]) for d in datamap[key])


def _unique_everseen(iterable: Iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen.

    Taken from: https://docs.python.org/3/library/itertools.html

    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def _get_dependencies_from_normalized_datamap(
    datamap: dict,
    key: Hashable,
    _seen: frozenset = None,
    _cache: dict = None,
) -> List[List[Hashable]]:
    """Return a list of dependency paths from `datamap` that lead to `key`."""
    seen = frozenset() if _seen is None else copy.copy(_seen)
    seen = seen.union([key])

    if _key_is_required_from_context(datamap, key):
        return [None]

    immediate_dependencies_not_already_seen = filter(seen.isdisjoint, _get_dependencies_for_key(datamap, key))

    _cache = {} if _cache is None else _cache

    def f(k):
        key = (k, seen)
        if result := _cache.get(key):
            return result
        result = _get_dependencies_from_normalized_datamap(datamap, k, seen, _cache)
        _cache[key] = result
        return result

    all_paths = []
    for dependency_set in immediate_dependencies_not_already_seen:
        deps_of_deps = product(*map(f, dependency_set))

        for dependency_path in deps_of_deps:
            if None in dependency_path:
                # this means it is circular
                continue
            dependency_paths_reversed = map(reversed, dependency_path)
            grand_parents = chain.from_iterable(dependency_paths_reversed)
            all_deps = chain(grand_parents, copy.copy(dependency_set), [key])
            all_paths.append(list(reversed(list(_unique_everseen(all_deps)))))

    if all_paths == []:
        return [None]

    return all_paths


def _get_dependencies(datamap: dict, key: Hashable) -> list:
    datamap_normed = _normalize_data_map(datamap)
    if not _is_valid_normalized_data_map(datamap_normed):
        msg = _normalized_data_map_validation_error(datamap_normed)
        raise ValueError(msg)
    dependencies = _get_dependencies_from_normalized_datamap(datamap_normed, key)

    if dependencies == [None]:
        raise PlanNotFoundError(
            "There was no plan found in the datamap. "
            f"No further progress on the plan could be found at key {key.__repr__()}. "
            "This may be due to circularity."
        )
    return dependencies
