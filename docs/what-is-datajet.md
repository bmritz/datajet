# What is datajet?

Datajet is a framework for working with complex dependencies in data. It allows the user to declare all datapoints and immediate dependencies of a system in a [DataMap](./datamap-reference.md), then query the dependency graph for any included datapoints, given a set of inputs. Datajet in effect "abstracts away" function calls, allowing the user to "just give inputs and get outputs" to a system of datapoints and dependencies.

```python
import datajet

datamap = {
    "dollars": datajet.common_resolvers.required_from_context(),
    "units": datajet.common_resolvers.required_from_context(),
    "prices": lambda dollars, units: [d/u for d, u in zip(dollars, units)],
    "average_price": lambda prices: sum(prices) / len(prices) * 1000 // 10 / 100
}

execute(
    datamap,
    fields=['average_price'],
    context={"dollars": [3.99, 10.47, 18.95,],"units": [1, 3, 5,]}
)
{'average_price': 3.75}
```