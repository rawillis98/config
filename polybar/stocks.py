#!/usr/bin/env python3

import json
import sys
import requests

output = ""
watchlist = ["SPX", "MSFT", "GOOG"]
for i, stock in enumerate(watchlist):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=W03D"
    data = requests.get(url)
    if int(data.status_code) != 200:
        print(f"Wrong status code: {data.status_code}")
        sys.exit(0)
    try:
        data = data.json()["Time Series (1min)"]
    except:
        if 'Note' in data.json():
            if data.json()['Note'].startswith("Thank you for using Alpha Vantage!"):
                print("Hit rate limit")
            else:
                print(data.json()['Note'])
        else:
            print(data.json())
        sys.exit(0)
    price = data[next(iter(data))]['4. close']
    price = round(float(price), 2)
    output += f"{stock}: ${price}"
    if i != len(watchlist) - 1:
        output += ", "
print(output)
