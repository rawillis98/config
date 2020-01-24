#!/home/alex/anaconda3/bin/python
from TDAPI import TDAPI


td = TDAPI()
accounts = td.get_accounts('positions')
account = accounts[0]['securitiesAccount']

out = ""
positions = account['positions']
if len(positions) > 0:
    for position in positions:
        instrument = position['instrument']
        symbol = instrument['symbol']
        qty = position['longQuantity']
        marketValue = position['marketValue'] / qty
        out += f"{symbol}x{int(qty)}@{marketValue}" + ", "
    out = out[:-2]
print(out)
