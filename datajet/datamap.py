"""A class for collecting resolvers."""

from typing import Callable, List, Optional

from ._normalization import _normalize_data_map


class DataJetMap(object):
    def __init__(self):
        self._map: dict = {}

    def register(self, output: Optional[str] = None, inputs: Optional[List[str]] = None):
        """Decorator function to register the decorated function as a part of this datamap.

        Args:
            output: The output DataPoint identifier for the decorated function.
                    Defaults to the function name.

            inputs: The DataPoint identifiers for the inputs into the resolver.
                    Defaults to the names of the arguments of the decorated function.

        Example:
            from datajet import DataJetMap

            data_map = DataJetMap()

            @data_map.register()
            def sales():
                return 4

            @data_map.register()
            def units():
                return 2

            @data_map.register()
            def price(sales, units):
                return sales/units

            data_map.data_map
            {'sales': [{'in': [], 'f': <function __main__.sales()>}],
            'units': [{'in': [], 'f': <function __main__.units()>}],
            'price': [{'in': ['sales', 'units'], 'f': <function __main__.price(sales, units)>}]}

        """

        def func(f: Callable):
            key = output if output is not None else f.__name__
            resolver_list = self._map.setdefault(key, [])
            if inputs is not None:
                to_append = {"in": inputs, "f": f}
            else:
                to_append = {"f": f}

            resolver_list.append(to_append)

        return func

    @property
    def data_map(self):
        return _normalize_data_map(self._map)
