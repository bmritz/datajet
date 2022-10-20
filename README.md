# DataJet

A Data Dependency Graph Framework and Executor

**Key Features**
- Lazy: Only Evaluate and return the data you need
- Declarative: Declare Data Dependencies and transformations explicitly, using plain python
- Dependency-Free: Just Python. 

## Installation
Requirements:
- Python >=3.8

To Get Started, Install DataJet From pypi:
```bash
pip install datajet
```
## Full Documentation
[https://bmritz.github.io/datajet/](https://bmritz.github.io/datajet/)

## Usage
DataJet dependencies are expressed as a `dict`. Each key-value pair in the dict corresponds to a piece of data and specifies how to calculate it:

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

You can also override any data declaration at "execute time":
```python
execute(
        datajet_map, 
        context={"dollars": map(lambda x: x*2, [3.99, 10.47, 18.95, 15.16,])}, 
        fields=['average_price']
)
{'average_price': 7.52}
```

Keys can be any hashable. The value corresponding to each key can be a function or an object. The functions can have 0 or more parameters. The parameter names must correspond to other keys in the dict if no explicitly defined inputs to the callable are declared in the map. See [Datamap reference](./docs/datamap-reference.md) for how to explicitly define inputs.

You can also define multiple ways of calculating a piece of data via defining a list of functions as the value to the key. Again, each function's parameters must correspond to other keys in the dict, or else you can define which other keys should be inputs to the function via explicitly defining inputs.

This framework frees you (the coder) from the need for more global knowledge about how pieces of data are connected when you request data. To define a datapoint you only need local knowledge of it's immediate inputs, and datajet finds the fastest path from the data you input to what you need.


## Development
```
git clone
make install
```
This will start a [poetry shell](https://python-poetry.org/docs/cli/#shell) that has all the dev dependencies installed.

### Development troubleshooting
If you see:
```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>
```
Go to /Applications/Python3.x and run 'Install Certificates.command'

## Built on ideas inspired by
- [wilkerlucio/Pathom3](https://github.com/wilkerlucio/pathom3)
- [stitchfix/hamilton](https://github.com/stitchfix/hamilton)
