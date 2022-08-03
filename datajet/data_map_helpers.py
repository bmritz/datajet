import copy
import graphlib
from functools import partial as p
from itertools import chain
import itertools
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
import uuid
def bfs(datamap, key, seen=None, queue=None, accum=None):
    # graph = {k: v[0]['in'] for k, v in normalized_data_map.items()}
    uid = str(uuid.uuid4())[:8]
    print()
    print("******* calling function *****")
    print(f"key: {key}")
    print(f"seen: {seen}")
    print(f"queue: {queue}")
    print(f"accum: {accum}")
    print(f"uid: {uid}")
    print("********")
    graph = datamap
    # Track the visited and unvisited nodes using queue
    seen = set() if seen is None else copy.deepcopy(seen)
    if queue is None:
        queue = collections.deque([key]) 
    else:
        queue = copy.deepcopy(queue)
    seen.add(key)
    # queue.append(key)
    # seen, queue = set([startnode]), collections.deque([startnode])
    accum = [] if accum is None else copy.deepcopy(accum)
    while queue:
        vertex = queue.popleft()
        accum.append(vertex)

        accum_over_possible_inputs = []
        for set_of_possible_inputs in graph[vertex]:
            # split out the state
            
            seen_copy = copy.deepcopy(seen)
            queue_copy = copy.deepcopy(queue) 
            for node in set_of_possible_inputs['in']:  
                if node not in seen_copy:
                    seen_copy.add(node)
                    queue_copy.append(node)

            acc = []
            acc2 = []
            for k in set_of_possible_inputs['in']:
                new_ancestors = bfs(datamap, k, seen_copy, None, None)
                acc = acc + [n for n in new_ancestors if n not in acc]
                if acc2 == []:
                    acc2 = new_ancestors
                else:
                    acc2 = [n+a for n in new_ancestors for a in acc2]
                print(f"new_ancestors: {new_ancestors}")
                print(f"acc: {acc}")
                print(f"acc2: {acc2}")
            ancestor_combos = list(itertools.product(*acc2))
            print(f"ancestor_combos: {list(copy.deepcopy(ancestor_combos))}")
            if len(ancestor_combos) > 1:
                ancestor_combo_starmap = list(itertools.starmap(extend, ancestor_combos))
            else:
                ancestor_combo_starmap = ancestor_combos
            print(f"ancestor_combo_starmap: {(copy.deepcopy(ancestor_combo_starmap))}")
            # breakpoint()
            for path in ancestor_combo_starmap:
                # if acc is None:
                #     acc = [y.extend(ancestor) for y in ancestor]
                accum_copy = copy.deepcopy(accum)
                # accum_copy
                print(f"path: {path}")
                accum_over_possible_inputs.append(accum_copy+list(path))
            # res = [bfs(datamap, k, seen_copy, None, accum_copy) for k in set_of_possible_inputs['in']]
            # print(f"res1: {res}")
            # if res:
            #     #res = list(itertools.chain.from_iterable(res))
            #     print(f"res2: {res}")
            #     accum_over_possible_inputs.extend(res)
            print(f"accum_over_possible_inputs: {accum_over_possible_inputs}")
        if accum_over_possible_inputs:
            # accum.append(accum_over_possible_inputs)
            print("**** RETURNING INNER *****")
            print(f"uid: {uid}")
            print(f"accum: {accum}")
            print(f"accum_over_possible_inputs: {accum_over_possible_inputs}")
            return accum_over_possible_inputs
    print("**** RETURNING *****")
    print(f"uid: {uid}")
    print(f"accum: {accum}")
    return accum
#######



###############


import collections
def graphsearch(normalized_data_map, startnode):
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

###############





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
