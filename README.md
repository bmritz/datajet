# DataJet

A Data Dependency Graph Framework and Executor

**Key Features**
- Lazy: Only Evaluate and return the data you need
- Declarative: Declare Data Dependencies and transformations explicitly, using plain python
- Dependency-Free: Just Python. 

## Installation
Requirements:
- Python >=3.6

To Get Started, Install DataJet From pypi:
```bash
pip install datajet
```

## Usage
DataJet dependencies are expressed as a `dict`. Each key-value pair in the dict corresponds to a piece of data and specifies how to calculate it:

```python
from datajet import execute
datajet_map = {
    "dollars": [3.99, 10.47, 18.95, 15.16,],
    "units": [1, 3, 5, 4,],
    "average_retail_price": lambda dollars, units: [d/u for d, u in zip(dollars, units)]
}
execute(datajet_map, fields=['average_retail_price'])
{'average_retail_price': [3.99, 3.49, 3.79, 3.79])}
```

You can also override any data declaration at "execute time":
```python
execute(
        datajet_map, 
        context={"dollars": map(lambda x: x*2, [3.99, 10.47, 18.95, 15.16,])}, 
        fields=['average_retail_price']
)

```

Keys can be any valid dict key. Values can be callables, objects, or a list of callables or objects. The callables can have 0 or more parameters. The parameter names must correspond to other keys in the dict if no explicitly defined inputs to the callable are declared in the map. (See [data maps](./data_map.md) for how to explicitly define inputs.)

The benefits of specifying your data like this may not be immediately apparent, but this gets powerful when you create many possible functions:

```python
from datajet import execute 
departments =[
    {"tag": "GR", "value": "GROCERY"}, {"tag": "FZ", "value": "FROZEN"}
]

categories = [
    {"tag": "PB", "value": "Peanut Butter", "department_tag": "GR"},
    {"tag": "J", "value": "Jelly", "department_tag": "GR",},
    {"tag": "FZE", "value":"FROZEN ENTREES", "department_tag": "FZ"}
]

subcategories = [
    {"tag": "NPB", "value": "PEANUT BUTTER - NATURAL", "category_tag": "PB"},
    {"tag": "CPB", "value": "PEANUT BUTTER - CONVENTIONAL", "category_tag": "PB"}
]

datajet_map = {
    "category": [
        lambda category_tag: dict((d['tag'], d['value']) for d in categories).get(category_tag),
    ],
    "category_tag": [
        lambda category: dict((d['value'], d['tag']) for d in categories).get(category),
        lambda subcategory: dict((d['value'], d['category_tag']) for d in subcategories).get(subcategory),
    ],
    "subcategory": [
        lambda subcategory_tag: dict((d['tag'], d['value']) for d in subcategories).get(subcategory_tag)
    ],
    "department_tag": [
        lambda category: dict((d['value'], d['department_tag']) for d in categories).get(category),
    ],
    "department": [
        lambda department_tag: dict((d['tag'], d['value']) for d in departments).get(department_tag),
    ],
}
execute(datajet_map, context={"subcategory_tag": "NPB"}, fields={"department_tag"})

{'department_tag': 'GR'}
```

It frees you (the coder) from the need for more global knowledge about how pieces of data are connected when you request data. To define a datapoint you only need local knowledge of it's immediate inputs, and datajet finds the fastest path from the data you input to what you need.


## Development
```
git clone
make install
```

If you see: 
```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>
```
Go to /Applications/Python3.x and run 'Install Certificates.command'
