"""
1. Get the tradable ticker symbols
Exchange: Poloniex
"""

import requests 
import json

# url = "https://poloniex.com/public?command=returnTicker"
# url = "https://api.poloniex.com/v2/currencies"
url = 'https://api.poloniex.com/markets/ticker24h'
req = requests.get(url)
# print(req)
coin_json = json.loads(req.text)
coin_list = []
for pair in coin_json:
    coin_list.append(pair['symbol'])

print(len(coin_list))

