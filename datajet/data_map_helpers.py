import copy
from itertools import chain, filterfalse, product
from typing import Hashable, Iterable, List

from .normalization import _normalize_data_map
from .validations import (
    _is_valid_normalized_data_map,
    _normalized_data_map_validation_error,
)


class PlanNotFoundError(ValueError):
    pass


def _get_dependencies_for_key(datamap: dict, key: Hashable) -> Iterable[List[Hashable]]:
    """Return a list of the different potential 'paths' to a `key` in `datamap`.

    Parameters:
        datamap: A "normalized" dict that represents the data depdendencies.
        key: The key in the datamap dict to get the dependencies for.

    """
    yield from (list(d["in"]) for d in datamap[key])


def _unique_everseen(iterable, key=None):
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
    seen: set = None,
) -> List[List[Hashable]]:
    """Return a list of dependency paths from `datamap` that lead to `key`."""
    seen = set() if seen is None else copy.copy(seen)
    seen.add(key)

    immediate_dependencies_not_already_seen = filter(seen.isdisjoint, _get_dependencies_for_key(datamap, key))

    def f(k):
        return _get_dependencies_from_normalized_datamap(datamap, k, seen)

    all_paths = []

    n_loops = 0
    n_stops_for_circularity = 0
    for dependency_set in immediate_dependencies_not_already_seen:
        deps_of_deps = product(*map(f, dependency_set))

        for dependency_path in deps_of_deps:
            n_loops += 1
            if None in dependency_path:
                # this means it is circular
                n_stops_for_circularity += 1
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
