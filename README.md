# DataJet

A Data Dependency Graph Framework and Executor

DataJet abstracts over function calls by mapping inputs through a graph of functions to desired outputs. As a programmer, you declare your data transformations (functions) once, with inputs and outputs, and datajet will handle mapping *any* input to *any* output reachable by the graph of functions.

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

Notes:
Before and after:
make the data transformation more declarative than imperative
simpler example of a more pure use case
json or yaml representation of the execute

### Before and After DataJet
<!-- prettier-ignore -->
<table>
  <thead>
    <tr>
      <th width="500px">Before DataJet</th>
      <th width="500px">After DataJet</th>
    </tr>
  </thead>
  <tbody>
  <tr width="600px">
      <td>

```python
dollars = [7.98, 20.94, 37.9, 30.32]
units =  [1, 3, 5, 4,]

def prices_from_dollars_and_units(dollars, units):
    return [d/u for d, u in zip(dollars, units)]

def average_price_from_prices(prices):
    return sum(prices) / len(prices) 

def average_price_rounded_from_average_price(average_price):
    return average_price * 1000 // 10 / 100

prices = prices_from_dollars_and_units(dollars, units)
average_price = average_price_from_prices(prices)
average_price_rounded = average_price_rounded_from_average_price(average_price)
average_price_rounded
7.52
```
</td>
<td>

```python
dollars = [7.98, 20.94, 37.9, 30.32]
units =  [1, 3, 5, 4,]

def prices(dollars, units):
    return [d/u for d, u in zip(dollars, units)]

def average_price(prices):
    return sum(prices) / len(prices) 

def average_price_rounded(average_price):
    return average_price * 1000 // 10 / 100


from datajet import execute

datajet_map = {
    "prices": prices,
    "average_price": average_price,
    "average_price_rounded": average_price_rounded,
}
execute(
        datajet_map,
        context={
            "dollars": dollars,
            "units": units,
        }, 
        fields=['average_price_rounded']
)
{'average_price_rounded': 7.52}
```

</td>
<td>


</td>
</tr>

</tbody>
</table>

## QuickStart

Say you have a monopoly on the local lemonade market. You have double-digit figure operation going slinging 4 yummy lemonade flavors: Original, Pink Lemonade, Strawberry Lemonade (my personal favorite), and Diet Lemonade (for those watching their figure). Demand for these various lemonades are different, and you, being the typical greedy capitalist corner lemonade stand owner you are, wish to capture as much [Consumer Surplus](https://en.wikipedia.org/wiki/Economic_surplus#Consumer_surplus) as you can, so price your lemonades differently based on flavor. 

Sales are good You have a 
### Before DataJet
Your options are either to go imperative:
```python
dollars = [7.98, 20.94, 37.9, 30.32]
units =  [1, 3, 5, 4,]
def prices_from_dollars_and_units(dollars, units):
    return [d/u for d, u in zip(dollars, units)]

def average_price_from_prices(prices):
    return sum(prices) / len(prices) 

def average_price_rounded_from_average_price(average_price):
    return average_price * 1000 // 10 / 100

prices = prices_from_dollars_and_units(dollars, units)
average_price = average_price_from_prices(prices)
average_price_rounded = average_price_rounded_from_average_price(average_price)
average_price_rounded
7.52
```
or, to compose functions (better):
```python
dollars = [7.98, 20.94, 37.9, 30.32]
units =  [1, 3, 5, 4,]
def prices(dollars, units):
    return [d/u for d, u in zip(dollars, units)]

def average_price(dollars, units):
    prices_ = prices(dollars, units)
    return sum(prices_) / len(prices_) 

def average_price_rounded(dollars, units):
    average_price_ = average_price(dollars, units)
    return average_price_ * 1000 // 10 / 100

average_price_rounded(dollars, units)
7.52
```

The problem with the second way, is say, you don't start with dollars and units, but instead start with prices:
```python
prices = [7.98, 6.98, 7.58, 7.58]
```

This would require a refactor:
```python
prices = [7.98, 6.98, 7.58, 7.58]

def average_price_from_prices(prices):
    return sum(prices) / len(prices) 

def average_price_rounded_from_prices(prices):
    average_price_ = average_price_from_prices(prices)
    return average_price_ * 1000 // 10 / 100

average_price_rounded_from_prices(prices)
7.52
```

Now, you're stuck with two functions to get the average price rounded, with the one to use depending on what data you have available at runtime. We can do better.


```python
from datajet import execute

dollars = [7.98, 20.94, 37.9, 30.32]
units =  [1, 3, 5, 4,]

def prices(dollars, units):
    return [d/u for d, u in zip(dollars, units)]

def average_price(prices):
    return sum(prices) / len(prices) 

def average_price_rounded(average_price):
    return average_price * 1000 // 10 / 100


datajet_map = {
    "prices": prices,
    "average_price": average_price,
    "average_price_rounded": average_price_rounded,
}
execute(
        datajet_map,
        context={
            "dollars": dollars,
            "units": units,
        }, 
        fields=['average_price_rounded']
)
{'average_price_rounded': 7.52}
```
And, if you have prices, you can directly get what you need:
```python
prices = [7.98, 6.98, 7.58, 7.58]
execute(
        datajet_map,
        context={
            "prices": prices,
        }, 
        fields=['average_price_rounded']

)
{'average_price_rounded': 7.52}
```

## Wordy Details 

Keys can be any hashable. The value corresponding to each key can be a function or an object. The functions can have 0 or more parameters. The parameter names must correspond to other keys in the dict if no explicitly defined inputs to the callable are declared in the map. See [Datamap reference](./docs/datamap-reference.md) for how to explicitly define inputs.

You can also define multiple ways of calculating a piece of data via defining a list of functions as the value to the key. Again, each function's parameters must correspond to other keys in the dict, or else you can define which other keys should be inputs to the function via explicitly defining inputs.

This framework frees you (the coder) from the need for more global knowledge about how pieces of data are connected when you request data. To define a datapoint you only need local knowledge of it's immediate inputs, and datajet finds the fastest path from the data you input to what you need.

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
