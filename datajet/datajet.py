import graphlib
from functools import partial as p
from itertools import chain

from .data_map_helpers import get_dependencies
from .normalization import _normalize_data_map
from .validations import is_valid_normalized_data_map


def execute(data_map: dict, fields: list, context: dict = None) -> dict:
    if context is not None:
        data_map.update(context)
    data_map = _normalize_data_map(data_map)
    if not is_valid_normalized_data_map(data_map):
        raise ValueError("Data map is not valid.")

    dependencies = set(chain(*map(p(get_dependencies, data_map), fields)))

    results = {}
    for dep in dependencies + fields:
        f = data_map[dep]["f"]
        inputs = data_map[dep].get("in", [])
        result = f(*[results[in_] for in_ in inputs])
        results[dep] = result

    for to_delete in dependencies.difference(fields):
        results.pop(to_delete)

    return results
