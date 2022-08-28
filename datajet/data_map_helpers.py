import collections
import copy
from typing import Hashable

from .normalization import _normalize_data_map
from .validations import _is_valid_normalized_data_map


class PlanNotFoundError(ValueError):
    pass


def _get_dependencies_from_normalized_datamap(
    datamap: dict,
    key: Hashable,
    seen: set = None,
) -> list:
    # Track the visited and unvisited nodes using queue
    seen = set() if seen is None else copy.copy(seen)
    queue = collections.deque([key])
    seen.add(key)
    accum = []
    while queue:
        vertex = queue.popleft()
        accum.append(vertex)

        accum_over_possible_inputs = []
        possible_inputs = [d["in"] for d in datamap[vertex]]
        for inputs in possible_inputs:
            acc = []
            circular = False
            for input_ in inputs:
                if input_ in seen:
                    circular = True
                    break
                try:
                    new_ancestors = _get_dependencies_from_normalized_datamap(
                        datamap,
                        input_,
                        seen,
                    )
                except PlanNotFoundError:
                    circular = True
                    break
                if acc == []:
                    acc = new_ancestors
                else:
                    acc = [a + [x for x in n if x not in a] for n in new_ancestors for a in acc]
            if circular:
                continue
            for path in acc:
                accum_over_possible_inputs.append(accum + list(path))

        if accum_over_possible_inputs:
            return accum_over_possible_inputs
    if circular:
        raise PlanNotFoundError
    return [accum]


def _get_dependencies(datamap: dict, key: Hashable) -> list:
    datamap_normed = _normalize_data_map(datamap)
    if not _is_valid_normalized_data_map(datamap_normed):
        raise ValueError("Data map is not valid.")
    return _get_dependencies_from_normalized_datamap(datamap_normed, key)
