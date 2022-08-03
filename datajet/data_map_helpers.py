import copy
import graphlib
from functools import partial as p
from multiprocessing.sharedctypes import Value
from typing import Hashable

from .normalization import _normalize_data_map
from .validations import is_valid_normalized_data_map
"""
this function depends on it being a dag because we need the static order -- we only need the order for sorting order of execution
We'll need to get more complicated in how we track the dependencies
"""
#######
import collections
# class graph:
#    def __init__(self,gdict=None):
#       if gdict is None:
#          gdict = {}
#       self.gdict = gdict

# def marked(n):
#    print(n)
# from itertools import repeat
# def zip_longest(*args, fillvalue=None):
#     # zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
#     SENTINEL = object()
#     iterators = [iter(it) for it in args]
#     num_active = len(iterators)
#     num_exhausted = 0
#     if not num_active:
#         return
#     values = [fillvalue]*len(iterators)
#     while True:
#         for i, it in enumerate(iterators):
#             try:
#                 value = next(it)
#             except StopIteration:
#                 num_active -= 1
#                 if not num_active:
#                     return
#                 iterators[i] = repeat(SENTINEL)
#                 # value = fillvalue
#             # values.append(value)
#             else:
#                 if value is not SENTINEL:
#                     values[i] = value
#         yield tuple(values)


def extend(ll, newlist):
    ll_cp = copy.deepcopy(ll)
    ll_cp.extend(newlist)
    return ll_cp

class PlanNotFoundError(ValueError):
    pass

from functools import partial
import inspect
def get_dependencies_from_normalized_datamap(datamap, key, seen=None,):
    # Track the visited and unvisited nodes using queue
    print()
    print("**********CALLING FUNCTION**********")
    print(f"{key=}")
    print(f"{seen=}")
    seen = set() if seen is None else copy.deepcopy(seen)

    queue = collections.deque([key]) 
    seen.add(key)

    accum = []
    while queue:
        vertex = queue.popleft()
        accum.append(vertex)

        accum_over_possible_inputs = []
        for set_of_possible_inputs in datamap[vertex]:
            # split out the state
            # seen_copy = seen.union(set_of_possible_inputs['in'])

            # seen_copy = copy.deepcopy(seen)
            composed_f = set_of_possible_inputs['f']
            argspec = inspect.getargspec(composed_f)
            if not set_of_possible_inputs['in']:
                print(f'Returning composed f')
                print(f'{composed_f=}')
                return [composed_f]
            print(f"{argspec=}")
            acc = []
            circular = False
            
            for k in set_of_possible_inputs['in']:
                if k in seen:
                    raise PlanNotFoundError
                try:
                    new_ancestors = get_dependencies_from_normalized_datamap(datamap, k, seen,)
                except PlanNotFoundError:
                    circular = True
                    break
                # argspec = inspect.getargspec(new_ancestors)
                # print(f"{argspec=}")
                # acc.append(new_ancestors)
                print(f'{new_ancestors=}')
                acc.append(new_ancestors)
                # if acc == []:
                #     acc = new_ancestors
                # else:
                #     acc = [a+[x for x in n if x not in a]  for n in new_ancestors for a in acc]
                    # seen.add(k)
                print(f"{acc=}")
            # return acc
            if circular:
                continue
            f = set_of_possible_inputs['f']
            if acc == []:
                accum_over_possible_inputs
            for path in [acc]:
                print(f"{path=}")
                argspec = inspect.getargspec(f)
                print(f"{argspec=}")
                f_partial = partial(f, *path)
                # print('parital complete')
                # accum_over_possible_inputs.append(accum+list(path))
                accum_over_possible_inputs.append(f_partial)
                # print('append complete')
        if accum_over_possible_inputs:
            print("RETURNING ACCUM OVER")
            print(f'{accum_over_possible_inputs=}')
            return accum_over_possible_inputs
    if circular:
        raise PlanNotFoundError
    
    # to_ret = [accum]
    to_ret = [[set_of_possible_inputs['f']]]
    print("RETURNING")
    print(f"{to_ret=}")
    return to_ret
#######

def get_dependencies(datamap, key):
    datamap_normed = _normalize_data_map(datamap)
    if not is_valid_normalized_data_map(datamap_normed):
        raise ValueError("Data map is not valid.")
    return get_dependencies_from_normalized_datamap(datamap_normed, key)

###############


# def _flatten(xss):
#     return [x for xs in xss for x in xs]


# def get_dependency_trees(normalized_data_map: dict, key: Hashable, dag: graphlib.TopologicalSorter) -> list:
#     edges = normalized_data_map[key]
#     dependencies = []
#     for edge in edges:
#         inputs = copy.deepcopy(edge["in"])
#         if inputs:
#             dependencies.append(inputs)

#     for tree_branch in dependencies:
#         deeper_dependencies = map(p(get_dependency_trees, normalized_data_map), tree_branch)
#         deeper_dependencies = list(deeper_dependencies)
#         tree_branch.extend([dep for dep in deeper_dependencies if dep])

#     #     dependencies.extend(chain(*map(p(get_dependency_trees, data_map_copy), inputs)))
#     return dependencies

# def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
#     def path(root,st,p):
#         if root is None:
#             return
#         if root.right is None and root.left is None:
#             p.append(st+"->"+str(root.val))
#         else:
#             st=st+"->"+str(root.val) if st!="" else str(root.val)
#             path(root.left,st,p)
#             path(root.right,st,p)
#     st=""
#     p=[]
#     if root.left==root.right==None:
#         return [str(root.val)]
#     path(root,st,p)
#     return p

# def path(edges,st,p,key,normalized_data_map):
#     if edges is None:
#         return
#     if len(edges) == 1:
#         p.append(st+"->"+str(edges[0]['in']))
#     # if root.right is None and root.left is None:
#     #     p.append(st+"->"+str(root.val))
#     else:
#         st=st+"->"+str(key) if st!="" else str(key)
#         for edge in edges:
#             path(normalized_data_map[edge['in'][0]], st, p, edge['in'][0], normalized_data_map)
#         # path(root.left,st,p)
        # path(root.right,st,p)

# def get_dependency_trees(normalized_data_map: dict, key: Hashable, _dag= None) -> list[graphlib.TopologicalSorter]:
#     edges = normalized_data_map[key]
#     st=""
#     p=[]
#     path(edges, st, p, key, normalized_data_map)
#     return p



# def get_one_level_deeper(datamap, key,):
#     return [
#         (key, copy.deepcopy(d['in'])) for d in datamap[key]
#     ]

# def get_dependency_trees(normalized_data_map: dict, key: Hashable, _dag= None) -> list[graphlib.TopologicalSorter]:
#     # assert isinstance(key, (list, tuple))

#     dag_orig = [] if _dag is None else _dag

#     new_dags = []
#     for level in get_one_level_deeper(normalized_data_map, key):
#         dag = copy.deepcopy(dag_orig)
#         dag.extend(level)


#     dags = []
#     edges = normalized_data_map[key]
#     dags_for_key = []
#     for i, edge in enumerate(edges):
#         dag = copy.deepcopy(dag_orig)
#         inputs = copy.deepcopy(edge["in"])
#         dag.append((key, inputs))
#         if inputs:
#             for input in inputs:
#                 dags_ = get_dependency_trees(normalized_data_map, input, dag)
#                 dags_for_key.extend(dags_)
#         else:
#             dags_=[dag]
#             dags_for_key.extend(dags_)
#     dags.extend(dags_for_key)

#     # return [dag_copy for dag in dags for dag_copy in get_dependency_trees(normalized_data_map, 
#     return dags


# def make_paths(dependency_tree):
#     paths = []
#     for direct_dependency_group in dependency_tree:
#         if not isinstance(direct_dependency_group, (list,)):
#             paths.append(direct_dependency_group)
#         else:
#             return [_flatten([paths, x]) for x in map(make_paths, direct_dependency_group)]
#     return paths


# def get_dependencies(data_map: dict, key) -> list:
#     deps = copy.deepcopy(data_map[key].get("in", []))
#     deps.extend(chain(*map(p(get_dependencies, data_map), deps)))

#     # get the correct order and dedup

#     sorter = graphlib.TopologicalSorter({k: v.get("in", []) for k, v in data_map.items()})
#     return [x for x in sorter.static_order() if x in deps]
