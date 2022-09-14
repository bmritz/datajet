import copy

from ._data_map_helpers import _get_dependencies
from ._normalization import _normalize_data_map
from ._validations import (
    _is_valid_normalized_data_map,
    _normalized_data_map_validation_error,
)
from .exceptions import RuntimeResolutionException


def execute(data_map: dict, fields: list, context: dict = None) -> dict:

    if context is not None:
        data_map = copy.copy(data_map)
        data_map.update(context)

    data_map = _normalize_data_map(data_map)
    if not _is_valid_normalized_data_map(data_map):
        msg = _normalized_data_map_validation_error(data_map)
        raise ValueError(msg)

    dependencies_for_each_field = [_get_dependencies(data_map, field) for field in fields]

    results = {}
    for possible_dependency_paths_for_specific_field in dependencies_for_each_field:
        possible_dependency_paths_for_specific_field = sorted(
            possible_dependency_paths_for_specific_field, key=lambda x: len(x)
        )
        for dependency_path_for_specific_field in possible_dependency_paths_for_specific_field:
            for dependency in reversed(dependency_path_for_specific_field):
                if dependency in results:
                    continue
                for d in data_map[dependency]:
                    inputs = d["in"]
                    if all(input_ in results for input_ in inputs):
                        f = d["f"]
                        try:
                            result = f(*[results[in_] for in_ in inputs])
                        except RuntimeResolutionException:
                            continue
                        else:
                            results[dependency] = result
                            break
                else:
                    # none of the paths to the dependency had inputs in the context and succeeded
                    # so, break out of 2nd for loop and start a different `dependency_path_for_specific_field`
                    break
            else:
                # break out of loop over possible paths if all dependencies in `dependency_path_for_specific_field` are resolved
                break
        else:
            raise RuntimeResolutionException
    for to_delete in set(results).difference(fields):
        results.pop(to_delete)
    return results
