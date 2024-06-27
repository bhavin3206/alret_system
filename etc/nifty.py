import requests
import json

# Download the JSON file
url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = requests.get(url, timeout=300)
data = response.json()

# Find the Bank Nifty token and symbol
bank_nifty_info = None
breakpoint()
for item in data:
    if item['name'] == 'NIFTY BANK' or item['symbol'] == 'BANKNIFTY':
        bank_nifty_info = item
        break

if bank_nifty_info:
    print(f"Bank Nifty Token: {bank_nifty_info['token']}")
    print(f"Bank Nifty Symbol: {bank_nifty_info['symbol']}")
else:
    print("Bank Nifty information not found.")
