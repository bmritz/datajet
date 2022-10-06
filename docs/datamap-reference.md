# DataMap Reference

Dependencies between datapoints in DataJet are declared in DataMaps, which are python dictionaries with a single key for each datapoint in the system.

## Normalized DataMaps

A normalized DataMap is the most verbose and regularized format of a DataMap. There are other acceptable schemas for datamaps that are accepted by `datajet.execute` (see [DataMap Shortcuts](#datamap-shortcuts)), however, it is helpful to first understand DataMaps in their normalized form to understand what a DataMap is declaring.

A DataMap is a normal python `dict`. Each key in the dictionary corresponds with a single datapoint in the dependency graph of the system. The dict key is the representation of the datapoint, you should choose a key with meaning. You could perhaps use tuples or namedtuples or dataclasses to specifically represent each datapoint to avoid conflicts.

The value corresponding to each key must be a `list` or `tuple`. The two are interchangeable. Each element of the list or tuple represents one potential "path" to the datapoint represented by the dict key. A path is a way to derive that datapoint--it is defined by a function and inputs to that function. Each path is represented by a python dict with the keys `"f"` and `"in"`. The value of `"f"` is a python function (called a "resolver function"), and the value of `"in"` must be a list of other datapoints defined as keys in the DataMap. To derive the datapoint, the function at `"f"` will be executed with the inputs from `"in"` passed to it as positional arguments.

### Example Normalized DataMap

```python
def is_below_freezing(temp, scale):
    if scale == "fahrenheit":
        return temp < 32
    if scale == "celsius":
        return temp < 0
    raise ValueError

data_map = {
    "temperature": [{"in": [], "f": lambda: 39}],
    "temperature_scale": [{"in": [], "f": lambda: "fahrenheit"}],
    "people_have_coats_on": [{"in": [], "f": lambda: True}],
    "temp_is_likely_below_freezing": [
        {"in": ["temperature", "temperature_scale"], "f": is_below_freezing},
        {"in": ["people_have_coats_on"], "f": lambda x: x},
    ]
}
```

In the above example, the datapoints `"temperature"`, `"temperature_scale"`, and `"people_have_coats_on"` are all "static" in the sense that those datapoints are not dependent on any other datapoints in the DataMap. `"temp_is_likely_below_freezing"` has 2 potential ways to calculate it -- one that uses `"temperature"` and `"temperature_scale"`, and one that derives whether the `"temp_is_likely_below_freezing"` from the `"people_have_coats_on"` datapoint. 

Here, the two paths to `"temp_is_likely_below_freezing"` is somewhat contrived, but one may want to specify two paths to a single datapoint in the case when it is not clear at "DataMap declaration time" what datapoints will have enough information to be calculated. You can tell datajet that a datapoint is expected to be provided at "execute time" by using the [`required_by_context` common resolver](./api.md#common-resolvers)

## DataMap Requirements
In addition to the above schema, `datajet` validates each DataMap for the following rules:
* Each datapoint listed in an `"in"` list must also be represented as a top-level key in the DataMap
* No extraneous keys, aside from `"in"` and `"f"`, can be present in any "path" dicts for any datapoints.
* The arity (number of arguments) for each resolver function at each `"f"` key must be equal to the length of the list at the corresponding `"in"` key, or else it must take a variable number of positional arguments that is compatable with the length of the list.


## DataMap shortcuts
The "normalized data map" is the internal datajet representation of a DataMap, and an acceptable schema for declaring DataMaps in your code. However, it is quite verbose. DataJet will allow several "shortcuts" when specifying your DataMap, to ease DataMap declaration:  

### Defining a single path with a `dict`
If you have only one path to a datapoint, you can forgo the list or tuple in the dict value and just write the dict that represents a single path.
```python
data_map_with_1_path = {
    "last-name": {"in": ["full-name"], "f": lambda fn: fn.split(" ")[-1]}
}
```

### Infering inputs from resolver arguments
If the string representation of the arguments of your resolver function match other datapoints, you can forgo specifying the `"in"` parameter, and only specify your function (as in `"al_east_teams_sorted"` below). DataJet will infer the input datapoint(s) by matching the string arguments to other keys in the DataMap.
```python
data_map = {
    "al_east_teams": {"f": lambda: ["Yankees", "Rays", "Blue Jays", "Orioles", "Red Sox"]},
    "al_east_teams_sorted": {"f": lambda al_east_teams: list(sorted(al_east_teams)})
}
```

DataJet will also accept a DataMap if you forgo the dict altogether and just give a resolver function as the value:
```python
data_map = {
    "al_east_teams": lambda: ["Yankees", "Rays", "Blue Jays", "Orioles", "Red Sox"],
    "al_east_teams_sorted": lambda al_east_teams: list(sorted(al_east_teams))
}
```

If the string representations of each argument to the resolver function are not found as other datapoints (keys) in the DataMap, the DataMap is invalid and `datajet.execute` will error.

### Defining Constants
In general, you can specify any constant DataPoints in your DataMap by simply declaring the constant as the dict value for the DataPoint Key. DataJet will infer if the constant does not conform to the expected dict or list schemas listed above, and treat the value as a constant if it does not.

```python
data_map = {
    "plate_appearance_results": ["hit", "walk", "hit", "ground out"],
    "n_at_bats": lambda plate_appearance_results: len([x for x in plate_appearance_results if x not in ('walk', 'hbp', 'sac')]),
    "n_hits": lambda plate_appearance_results: len([x for x in plate_appearance_results if x == 'hit']),
    'batting_avg': lambda n_hits, n_at_bats: n_hits/n_at_bats
}
```
In the datamap above, `"plate_appearance_results"` is declared as a constant.
