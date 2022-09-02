import copy

from .data_map_helpers import _get_dependencies
from .normalization import _normalize_data_map
from .validations import _is_valid_normalized_data_map


def execute(data_map: dict, fields: list, context: dict = None) -> dict:
    """Execute the resolvers in a data_map to return values for `fields` requested..

    Args:
        data_map: A data_map
        fields: A list of fields to return from the data map.
        context: A dict of values to send to the data map as context.

    """
    if context is not None:
        data_map = copy.copy(data_map)
        data_map.update(context)

    data_map = _normalize_data_map(data_map)
    if not _is_valid_normalized_data_map(data_map):
        raise ValueError("Data map is not valid.")

    dependencies = [_get_dependencies(data_map, field) for field in fields]

    results = {}
    for deps in dependencies:
        path_to_take = max(deps, key=lambda x: -len(x))
        for dep in reversed(path_to_take):
            if dep in results:
                continue
            for d in data_map[dep]:
                inputs = d["in"]
                if all(input_ in results for input_ in inputs):
                    f = d["f"]
                    break
            result = f(*[results[in_] for in_ in inputs])
            results[dep] = result

    for to_delete in set(results).difference(fields):
        results.pop(to_delete)

    return results
