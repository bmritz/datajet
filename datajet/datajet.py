import copy
import graphlib
from functools import partial as p
from itertools import chain

from .data_map_helpers import get_dependencies
from .normalization import _normalize_data_map
from .validations import is_valid_normalized_data_map



def execute(data_map: dict, fields: list, context: dict = None) -> dict:
    
    if context is not None:
        data_map = copy.copy(data_map)
        data_map.update(context)

    data_map = _normalize_data_map(data_map)
    if not is_valid_normalized_data_map(data_map):
        raise ValueError("Data map is not valid.")

    dependencies = [
        get_dependencies(data_map, field)
        for field in fields
    ]
    
    results = {}
    for deps in dependencies:
        path_to_take = max(deps, key=lambda x: -len(x))
        for dep in reversed(path_to_take):
            if dep in results:
                continue
            for d in data_map[dep]:
                inputs = d['in']
                if all(input_ in results for input_ in inputs):
                    f = d['f']
                    break
            # f, inputs = next(((d['f'], d['in']) for d in data_map[dep] ))
            result = f(*[results[in_] for in_ in inputs])
            results[dep] = result

    for to_delete in set(results).difference(fields):
        results.pop(to_delete)

    return results
