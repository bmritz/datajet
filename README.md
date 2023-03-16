# DataJet

A Data Dependency Graph Framework and Executor

DataJet abstracts over function calls by mapping inputs through a graph of functions to desired outputs. As a programmer, you declare your data transformations (functions of inputs to outputs) once, and datajet will handle mapping *any* input to *any* output reachable by the graph of functions.

**Key Features**
- Lazy: Only Evaluate and return the data you need
- Declarative: Declare Data and functions on the data explicitly, using plain python
- Dependency-Free: Just Python. 

## Installation
Requirements:
- Python >=3.8

To Get Started, Install DataJet From pypi:
```bash
pip install datajet
```

## Why would I use this?

- DataJet simplifies the codebase of dynamic systems with mutliple ways to calculate a datapoints from different inputs.
- DataJet de-couples downstream calculations from the mechanics of calculating upstream dependencies. 


## Quickstart

```python
from datajet import execute

dollars = [7.98, 20.94, 37.9, 30.31]
units =  [1, 3, 5, 4,]

def prices(dollars, units):
    return [d/u for d, u in zip(dollars, units)]

def average_price(prices):
    return sum(prices) / len(prices) 

def average_price_rounded_down(average_price):
    return average_price * 1000 // 10 / 100


datajet_map = {
    "prices": prices,
    "average_price": average_price,
    "average_price_rounded_down": average_price_rounded_down,
}
execute(
        datajet_map,
        context={
            "dollars": dollars,
            "units": units,
        }, 
        fields=['average_price_rounded_down']
)
{'average_price_rounded_down': 7.52}
```
And, if you have prices, you can directly get what you need:
```python
prices = [3.99, 4.49, 2.89, 2.79, 2.99]

execute(datajet_map,context={"prices": prices,}, fields=['average_price', 'average_price_rounded_down'])
{'average_price': 3.4299999999999997, 'average_price_rounded_down': 3.42}
```

## Important Details

Keys can be any hashable. The value corresponding to each key can be a function or an object. The functions can have 0 or more parameters. The parameter names must correspond to other keys in the dict if no explicitly defined inputs to the callable are declared in the map. See [Datamap reference](./docs/datamap-reference.md) for how to explicitly define inputs.

You can also define multiple ways of calculating a piece of data via defining a list of functions as the value to the key. Again, each function's parameters must correspond to other keys in the dict, or else you can define which other keys should be inputs to the function via explicitly defining inputs.


## Full Documentation
[https://bmritz.github.io/datajet/](https://bmritz.github.io/datajet/)

## Development


### To create the development environment locally:
```
git clone
make install
```
This will start a [poetry shell](https://python-poetry.org/docs/cli/#shell) that has all the dev dependencies installed. You can run `deactivate` to exit the shell.

### To run tests
```
make test
```

#### Development troubleshooting
If you see:
```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>
```
Go to /Applications/Python3.x and run 'Install Certificates.command'

## Built on ideas inspired by
- [wilkerlucio/Pathom3](https://github.com/wilkerlucio/pathom3)
- [stitchfix/hamilton](https://github.com/stitchfix/hamilton)
