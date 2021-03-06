#!/usr/bin/env python3

import configparser
import sys
import requests
from decimal import Decimal

config = configparser.ConfigParser()

# File must be opened with utf-8 explicitly
with open(r'/home/alex/.config/polybar/crypto-config', 'r', encoding='utf-8') as f:
	config.read_file(f)

# Everything except the general section
currencies = [x for x in config.sections() if x != 'general']
base_currency = config['general']['base_currency']
params = {'convert': base_currency}


for currency in currencies:
        icon = config[currency]['icon']
        response = requests.get(f'https://api.coinmarketcap.com/v1/ticker/{currency}', params=params)
        if response.status_code == 200:
            json = response.json()[0]
            local_price = round(Decimal(json[f'price_{base_currency.lower()}']), 2)
            change_24 = float(json['percent_change_24h'])

            display_opt = config['general']['display']
            if display_opt == 'both' or display_opt == None:
                    sys.stdout.write(f'{icon} ${local_price}/{change_24:+}%  ')
            elif display_opt == 'percentage':
                    sys.stdout.write(f'{icon} {change_24:+}%  ')
            elif display_opt == 'price':
                    sys.stdout.write(f'{icon} ${local_price}  ')
        elif response.status_code == 429:
            sys.stdout.write("Hit rate limit. Decrease interval in polybar config.")
            sys.exit(0)
        else:
            sys.stdout.write(f"Response {response.status_code}")
            sys.exit(0)
