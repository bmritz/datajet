# ✈️ DataJet 

[![Release](https://img.shields.io/github/v/release/bmritz/datajet)](https://img.shields.io/github/v/release/bmritz/datajet)
[![Build status](https://img.shields.io/github/workflow/status/bmritz/datajet/merge-to-main)](https://img.shields.io/github/workflow/status/bmritz/datajet/merge-to-main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/bmritz/datajet)](https://img.shields.io/github/commit-activity/m/bmritz/datajet)
[![License](https://img.shields.io/github/license/bmritz/datajet)](https://img.shields.io/github/license/bmritz/datajet)

DataJet is a Data Dependency Graph Framework and Executor with the following features:

- Lazy: Evaluate and return only the data you need
- Efficient: DataJet doesn't get in the way of performance
- Declarative: Declare Data Dependencies and transformations explicitly, using plain python
- Dependency-Free: Just Python. 

## Installation
Install via pip from PyPi:
```shell
pip install datajet
```

## Usage
Usage is simple:

```python
from datajet import execute

datajet_map = {
    "dollars": [3.99, 10.47, 18.95, 15.16,],
    "units": [1, 3, 5, 4,],
    "prices": lambda dollars, units: [d/u for d, u in zip(dollars, units)],
    "average_price": lambda prices: sum(prices) / len(prices) * 1000 // 10 / 100
}

execute(datajet_map, fields=['prices', 'average_price'])
# Result: 
# {'prices': [3.99, 3.49, 3.79, 3.79], 'average_price': 3.76}
```

Look at [What is DataJet](./what-is-datajet.md) to understand more, or jump straight into the [tutorial](./tutorial.md).
