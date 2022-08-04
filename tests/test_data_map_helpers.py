from unittest import expectedFailure

import pytest

from datajet.data_map_helpers import PlanNotFoundError, get_dependencies_from_normalized_datamap

datamap_1 = {
    "a": [{"in": ["b","e"], "f": lambda x: 1}, {"in": ["c"], "f": lambda x: 1}],
    "b": [{"in": ["d"], "f": lambda x: 1}, {"in": ["c"], "f": lambda x: 1}],
    "c": [{"in": [], "f": lambda: 1}],
    "d": [{"in": [], "f": lambda: 1}],
    "e": [{"in": [], "f": lambda: 1}],
}

datamap_2 = {
    "a": [{"in": ["b", "c"], "f": lambda x, y: 1}, {"in": ["c","d"], "f": lambda x: 1}],
    "b": [{"in": ["d","e"], "f": lambda x, y: 1}, {"in": ["f"], "f": lambda x: 1}],
    "c": [{"in": ["g","h"], "f": lambda x, y: 1}],
    "d": [{"in": ["i"], "f": lambda x: 1},{"in": ["j"], "f": lambda x: 1}],
    "e": [{"in": [], "f": lambda: 1},],
    "f": [{"in": [], "f": lambda: 1},],
    "g": [{"in": [], "f": lambda: 1},],
    "h": [{"in": [], "f": lambda: 1},],
    "i": [{"in": [], "f": lambda: 1},],
    "j": [{"in": [], "f": lambda: 1},],
}

datamap_3 = {
    "a": [{"in": ['b', 'c'], 'f': lambda x,y: 1}],
    "b": [{"in": [], 'f': lambda : 1}],
    "c": [{"in": [], 'f': lambda : 1}],
}

datamap_4 = {'a': [{'in': ['b', 'c'], 'f': lambda x,y: 3}],
 'b': [{'in': ['c'], 'f': lambda x: 2}],
 'c': [{'in': [], 'f':lambda: 2}]}


# test for circularity
datamap_5 = {
 'a': [{'in': ['b', 'c'], 'f': lambda x,y: 3}],
 'b': [{'in': ['c'], 'f': lambda x: 2}],
 'c': [{'in': ['a'], 'f':lambda: 2}],
}

# test that a non-circular path is found in presence of circular path
datamap_6 = {
 'a': [{'in': ['b', 'c'], 'f': lambda x,y: 3}, {'in': ['d', 'e'], 'f': lambda x,y: 3}],
 'b': [{'in': ['c'], 'f': lambda x: 2}],
 'c': [{'in': ['a'], 'f':lambda x: 2}],
 'd': [{'in': [], 'f':lambda: 2}],
 'e': [{'in': [], 'f':lambda: 2}],
}

datamap_7 = {
 'a': [{'in': [], 'f': lambda : 3}, ],
}

# test for circularity on two paths
datamap_8 = {
 'a': [{'in': ['b', 'c'], 'f': lambda x,y: x+y}, {'in': ['d'], 'f': lambda y: 3}],
 'b': [{'in': ['c'], 'f': lambda x: 2}],
 'c': [{'in': ['a'], 'f':lambda x: 2}],
 'd': [{'in': ['b'], 'f': lambda x: 2}],
}

@pytest.mark.parametrize("datamap,key,expected", [
    ( datamap_1 , 'a', [['a', 'b', 'd', 'e'], ['a', 'b', 'c', 'e'], ['a', 'c']]),
    ( datamap_1 , 'c', [['c']]),
    ( datamap_1 , 'b', [['b', 'd'], ['b', 'c']]),
    ( datamap_2 , 'a', [['a', 'b', 'd', 'i', 'e', 'c', 'g', 'h'],
 ['a', 'b', 'd', 'j', 'e', 'c', 'g', 'h'],
 ['a', 'b', 'f', 'c', 'g', 'h'],
 ['a', 'c', 'g', 'h', 'd', 'i'],
 ['a', 'c', 'g', 'h', 'd', 'j']]),
    ( datamap_2, 'b', [['b', 'd', 'i', 'e'], ['b', 'd', 'j', 'e'], ['b', 'f']]),
    ( datamap_2, 'c',  [['c', 'g', 'h']]),
    ( datamap_3, 'a',  [['a', 'b', 'c']]),
    ( datamap_4, 'a',  [['a', 'b', 'c']]),
    ( datamap_6, 'a',  [['a', 'd', 'e']]),
    ( datamap_7, 'a', [['a']]),
])
def test_get_dependencies_from_normalized_datamap(datamap, key ,expected):
    assert get_dependencies_from_normalized_datamap(datamap, key) == expected


@pytest.mark.parametrize("datamap,key,expected", [
    ( datamap_5, 'a', []),
    ( datamap_8, 'a', []),
])
def test_get_dependencies_from_normalized_datamap_raises(datamap, key ,expected):
    with pytest.raises(PlanNotFoundError):
        get_dependencies_from_normalized_datamap(datamap, key) == expected



# In [80]: for x in leaf:
#     ...:     if not isinstance(x, (list,)):
#     ...:         accum.append(x)
#     ...:     else:
#     ...:         acc= []
#     ...:         for y in x:
#     ...:             new_accum = copy.deepcopy(accum)
#     ...:             new_accum.append(y)
#     ...:             acc.append(new_accum)
#     ...:


# @pytest.mark.parametrize("input,expected",[
#     (['b', [['d'], ['c']]], [["b", "d"], ["b","c"]])
# ])
# def test_make_paths()