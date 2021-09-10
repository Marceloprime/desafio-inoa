import investpy

search_result = data = investpy.get_bond_historical_data(bond='Brazil 3Y', from_date='01/01/2015', to_date='01/01/2030')

print(search_result)
