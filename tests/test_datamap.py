
from datajet import DataJetMap


def test_data_map_works():

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
    
    assert set(data_map.data_map.keys()) == set(['sales', 'units', 'price'])
    assert all([len(ll)==1 for ll in data_map.data_map.values()])


def test_data_map_registers_multiple_of_same_function_name():

    data_map = DataJetMap()

    @data_map.register()
    def sales():
        return 4

    @data_map.register()
    def units(sales):
        return 2 * sales

    @data_map.register()
    def units(sales):
        return sales * 3
    
    assert set(data_map.data_map.keys()) == set(['sales', 'units'])
    assert len(data_map.data_map['units']) == 2
    assert len(data_map.data_map['sales']) == 1