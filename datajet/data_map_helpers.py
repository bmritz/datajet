import copy
import graphlib
from functools import partial as p
from itertools import chain

"""
this function depends on it being a dag because we need the static order -- we only need the order for sorting order of execution
We'll need to get more complicated in how we track the dependencies
"""


def _flatten(xss):
    return [x for xs in xss for x in xs]


def get_dependency_trees(normalized_data_map: dict, key) -> list:
    edges = normalized_data_map[key]
    dependencies = []
    for edge in edges:
        inputs = copy.deepcopy(edge["in"])
        if inputs:
            dependencies.append(inputs)

    for tree_branch in dependencies:
        deeper_dependencies = map(p(get_dependency_trees, normalized_data_map), tree_branch)
        deeper_dependencies = list(deeper_dependencies)
        tree_branch.extend([dep for dep in deeper_dependencies if dep])

    #     dependencies.extend(chain(*map(p(get_dependency_trees, data_map_copy), inputs)))
    return dependencies


def get_dependencies(data_map: dict, key) -> list:
    deps = copy.deepcopy(data_map[key].get("in", []))
    deps.extend(chain(*map(p(get_dependencies, data_map), deps)))

    # get the correct order and dedup

    sorter = graphlib.TopologicalSorter({k: v.get("in", []) for k, v in data_map.items()})
    return [x for x in sorter.static_order() if x in deps]
