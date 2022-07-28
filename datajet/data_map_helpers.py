import copy
import graphlib
from functools import partial as p
from itertools import chain
from os import get_terminal_size
from typing import Hashable

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

def bfs(normalized_data_map, startnode):
    graph = {k: v[0]['in'] for k, v in normalized_data_map.items()}
    # Track the visited and unvisited nodes using queue
    seen, queue = set([startnode]), collections.deque([startnode])
    accum = []
    while queue:
        vertex = queue.popleft()
        accum.append(vertex)
        for node in graph[vertex]:
            if node not in seen:
                seen.add(node)
                queue.append(node)
    return accum
#######







def _flatten(xss):
    return [x for xs in xss for x in xs]


def get_dependency_trees(normalized_data_map: dict, key: Hashable, dag: graphlib.TopologicalSorter) -> list:
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

def path(edges,st,p,key,normalized_data_map):
    if edges is None:
        return
    if len(edges) == 1:
        p.append(st+"->"+str(edges[0]['in']))
    # if root.right is None and root.left is None:
    #     p.append(st+"->"+str(root.val))
    else:
        st=st+"->"+str(key) if st!="" else str(key)
        for edge in edges:
            path(normalized_data_map[edge['in'][0]], st, p, edge['in'][0], normalized_data_map)
        # path(root.left,st,p)
        # path(root.right,st,p)

def get_dependency_trees(normalized_data_map: dict, key: Hashable, _dag= None) -> list[graphlib.TopologicalSorter]:
    edges = normalized_data_map[key]
    st=""
    p=[]
    path(edges, st, p, key, normalized_data_map)
    return p



def get_one_level_deeper(datamap, key,):
    return [
        (key, copy.deepcopy(d['in'])) for d in datamap[key]
    ]

def get_dependency_trees(normalized_data_map: dict, key: Hashable, _dag= None) -> list[graphlib.TopologicalSorter]:
    # assert isinstance(key, (list, tuple))

    dag_orig = [] if _dag is None else _dag

    new_dags = []
    for level in get_one_level_deeper(normalized_data_map, key):
        dag = copy.deepcopy(dag_orig)
        dag.extend(level)


    dags = []
    edges = normalized_data_map[key]
    dags_for_key = []
    for i, edge in enumerate(edges):
        dag = copy.deepcopy(dag_orig)
        inputs = copy.deepcopy(edge["in"])
        dag.append((key, inputs))
        if inputs:
            for input in inputs:
                dags_ = get_dependency_trees(normalized_data_map, input, dag)
                dags_for_key.extend(dags_)
        else:
            dags_=[dag]
            dags_for_key.extend(dags_)
    dags.extend(dags_for_key)

    # return [dag_copy for dag in dags for dag_copy in get_dependency_trees(normalized_data_map, 
    return dags


def make_paths(dependency_tree):
    paths = []
    for direct_dependency_group in dependency_tree:
        if not isinstance(direct_dependency_group, (list,)):
            paths.append(direct_dependency_group)
        else:
            return [_flatten([paths, x]) for x in map(make_paths, direct_dependency_group)]
    return paths


def get_dependencies(data_map: dict, key) -> list:
    deps = copy.deepcopy(data_map[key].get("in", []))
    deps.extend(chain(*map(p(get_dependencies, data_map), deps)))

    # get the correct order and dedup

    sorter = graphlib.TopologicalSorter({k: v.get("in", []) for k, v in data_map.items()})
    return [x for x in sorter.static_order() if x in deps]
