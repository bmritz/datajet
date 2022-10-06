# Core Concepts

## DataPoint
A DataPoint is a single "piece" of data that may be related to other datapoints via being an input to or output of [resolvers](#Resolvers). Each key in a `DataMap` corresponds to a single datapoint. A datapoint in other contexts is sometimes called an "attribute", "property", or "field" -- they are essentially the nodes on the data dependency graph.

!!! note

    A DataPoint is not necessarily a single _value_, it may be a series of data values, or a column of a dataset, or even a whole data table. The important part is that it is a unit of data that is derived in total from other units of data.

## Resolver
Resolvers are python functions that establish relationships between datapoints. A resolver relates the input datapoints, which correspond to arguments to the function, to the datapoint represented by the output of the function. Resolvers work with lambda or regular python functions defined with `def`, as well as functions cached with `functools.lru_cache`.

## DataMap
A DataMap is a declaration of all datapoints and associated dependency datapoints & resolvers in a system. A DataMap is declared as a regular python `dict` that must adhere to a particular schema--see [DataMap Reference](./datamap-reference.md) for more.