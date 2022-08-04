import collections
import copy
from typing import Hashable

from .normalization import _normalize_data_map
from .validations import is_valid_normalized_data_map


class PlanNotFoundError(ValueError):
    pass


def get_dependencies_from_normalized_datamap(
    datamap: dict,
    key: Hashable,
    seen: set = None,
):
    # Track the visited and unvisited nodes using queue
    print()
    print("**********CALLING FUNCTION**********")
    print(f"{key=}")
    print(f"{seen=}")
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
            # breakpoint()
            # split out the state
            # seen_copy = seen.union(set_of_possible_inputs['in'])

            # seen_copy = copy.deepcopy(seen)
            acc = []
            circular = False
            # breakpoint()
            for input_ in inputs:
                # breakpoint()
                if input_ in seen:
                    print("ERROR")
                    print(f"{input_=}")
                    print(f"{seen=}")
                    circular = True
                    break
                # if k not in seen:
                try:
                    print(f"{input_=}")
                    new_ancestors = get_dependencies_from_normalized_datamap(
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
                print(f"{acc=}")
                # seen.add(k)
            if circular:
                continue
            for path in acc:
                print(f"{path=}")
                accum_over_possible_inputs.append(accum + list(path))

        if accum_over_possible_inputs:
            return accum_over_possible_inputs
    if circular:
        raise PlanNotFoundError
    return [accum]


def get_dependencies(datamap, key):
    datamap_normed = _normalize_data_map(datamap)
    if not is_valid_normalized_data_map(datamap_normed):
        raise ValueError("Data map is not valid.")
    return get_dependencies_from_normalized_datamap(datamap_normed, key)
