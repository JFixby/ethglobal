import json

import requests

import K1inch

def fetch_tokens():
    CHAIN_ID = 1  # Ethereum Mainnet
    BASE_URL = f"https://api.1inch.dev/swap/v5.2/{CHAIN_ID}"
    TOKEN_LIST_URL = f"{BASE_URL}/tokens"

    headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {K1inch.API_KEY}"
    }

    response = requests.get(TOKEN_LIST_URL, headers=headers)

    tokens = response.json()["tokens"]

    # print(json.dumps(tokens, indent=2))
    result = {}
    # Lookup address by symbol
    for address, token in tokens.items():
        result[token["symbol"]] = address
    return result
