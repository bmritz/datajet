# Tutorial

## Create a data map

Your data processing can be expressed as a "flow" of outputs of functions into inputs of other functions. The datamap expresses the dependencies in your data.

A data map is a python `dict`. The keys of the dict are "addresses" of individual pieces data and are used to reference that piece of data. What is a "piece" of data, you ask? In other contexts, what I refer to as a piece of data may be called an "attribute of an entity" or a "node of a graph".  You can address your data with any hashable python data structure, but each address of data must be unique in the map. You are encouraged to address your data specifically to avoid conflicts, and to describe the data.

Each value of the dict must be a lists or tuple. They are interchangeable. Each value of the list or tuple is a dict that represents a "path" to that piece of data. A "path" consists of a function, represented by the key `"f"` in the dict, and inputs, represented by the key `"in"` in the dict. 

```python
data_map = {
    "category": 
}


```

### Datamap shortcuts
Above, you get the long version of how to create what is called a "normalized data map." The "normalized data map" is the internal datajet representation of a datamap. You can take several "shortcuts" when specifying your datamap, and datajet will create a normalized data map under the hood prior to execution:  

- If you have only one path to a data address, you can forgo the list or tuple in the dict value and just write a dict.
```python
data_map_with_1_path = {
    "category_from_upc": {"in": ["upc"], "f": query_db_for_category_via_upc}
}
```

- If the string representation of the parameters of your function match data_addresses, you can forgo specifying the `"in"` and `"f"` parameters, and only specify your function (as in `"al_east_teams_sorted"` below).    
```python
data_map = {
    "al_east_teams": lambda: ["Yankees", "Rays", "Blue Jays", "Orioles", "Red Sox"],
    "al_east_teams_sorted": lambda al_east_teams: list(sorted(al_east_teams))
}
```
