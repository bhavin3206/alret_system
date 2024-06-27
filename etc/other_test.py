# from nsetools import Nse

# # Create an instance of the Nse class
# nse = Nse()

# # Get the live data for the Bank Nifty index
# bank_nifty_data = nse.get_index_quote('BANKNIFTY')

# # Print the live data
# print(bank_nifty_data)


import requests
import json

while True:
    # URL for the NSE Bank Nifty index
    url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK'

    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    # Create a session
    session = requests.Session()
    session.get('https://www.nseindia.com', headers=headers)  # initial request to set the cookies

    # Fetch the data
    response = session.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data['data'][0]['lastPrice'])
        # breakpoint()
        # with open('data.json', 'w') as f:
        #     f.write(json.dumps(data, indent=4))  # Pretty print the JSON data
    else:
        print(f"Failed to fetch data: {response.status_code}")
