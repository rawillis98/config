#!/home/alex/anaconda3/bin/python
from TDAPI import TDAPI


td = TDAPI()
accounts = td.get_accounts('positions')
account = accounts[0]['securitiesAccount']

equity = account['currentBalances']['equity']
print(f"${equity}")




