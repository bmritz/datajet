# datajet

[![Release](https://img.shields.io/github/v/release/bmritz/datajet)](https://img.shields.io/github/v/release/bmritz/datajet)
[![Build status](https://img.shields.io/github/workflow/status/bmritz/datajet/merge-to-main)](https://img.shields.io/github/workflow/status/bmritz/datajet/merge-to-main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/bmritz/datajet)](https://img.shields.io/github/commit-activity/m/bmritz/datajet)
[![License](https://img.shields.io/github/license/bmritz/datajet)](https://img.shields.io/github/license/bmritz/datajet)

A DataPoint Dependency Graph Framework and Executor

## Getting Started
See the [Quickstart](./quickstart.md)


- Lazy: Only Evaluate and return the data you need
- Declarative: Declare Data Dependencies and transformations explicitly, using plain python
- Dependency-Free: Just Python. 

## Simple API

### `execute`

```python
from datajet import execute
datajet_map = {
    "dollars": [3.99, 10.47, 18.95, 15.16,],
    "units": [1, 3, 5, 4,],
    "prices": lambda dollars, units: [d/u for d, u in zip(dollars, units)],
    "average_price": lambda prices: sum(prices) / len(prices) * 1000 // 10 / 100
}
execute(datajet_map, fields=['prices', 'average_price'])
{'prices': [3.99, 3.49, 3.79, 3.79], 'average_price': 3.76}
```