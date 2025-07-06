import json

import requests
from web3 import Web3
from eth_account import Account

import K1inch
from CHAIN_ID import ETHERIUM, POLYGON





class OneInchClient:
    def __init__(self, chain_id=ETHERIUM, private_key=None, api_key=None):
        self.chain_id = chain_id
        self.base_url = f"https://api.1inch.dev/swap/v6.1/{chain_id}"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else ""
        }

        # Polygon RPC endpoint
        self.web3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))
        if not self.web3.is_connected():
            raise Exception("Failed to connect to Polygon RPC")

        self.account = Account.from_key(private_key) if private_key else None

    def get_token_address(self, symbol):
        url = f"{self.base_url}/tokens"
        response = requests.get(url, headers=self.headers)
        if not response.ok:
            raise Exception(f"Failed to fetch token list: {response.status_code} {response.text}")
        tokens = response.json()["tokens"]

        if symbol.upper() in ["MATIC", "ETH"]:
            return "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

        for address, token in tokens.items():
            if token["symbol"].upper() == symbol.upper():
                checksum_address = Web3.to_checksum_address(address)
                return checksum_address
        raise ValueError(f"Token symbol '{symbol}' not found")

    def get_quote(self, from_token, to_token, amount_wei):
        url = f"{self.base_url}/quote"
        params = {
            "fromTokenAddress": from_token,
            "toTokenAddress": to_token,
            "amount": str(amount_wei)
        }
        response = requests.get(url, headers=self.headers, params=params)
        if not response.ok:
            raise Exception(f"Failed to get quote: {response.status_code} {response.text}")
        return response.json()

    def build_swap_tx(self, from_token, to_token, amount_wei):
        url = f"{self.base_url}/swap"
        params = {
            "fromTokenAddress": Web3.to_checksum_address(from_token),
            "toTokenAddress": Web3.to_checksum_address(to_token),
            "amount": str(amount_wei),
            "fromAddress": self.account.address,
            "slippage": 1,
            "disableEstimate": "true"
        }
        response = requests.get(url, headers=self.headers, params=params)
        if not response.ok:
            raise Exception(f"Failed to build swap tx: {response.status_code} {response.text}")
        response = response.json()["tx"]
        response["chainId"] = self.chain_id
        return response

    def send_transaction(self, tx_data):
        # tx_data['chainId'] = chainId
        tx_data["from"] = Web3.to_checksum_address(tx_data["from"])
        tx_data["to"] = Web3.to_checksum_address(tx_data["to"])
        tx_data["nonce"] = self.web3.eth.get_transaction_count(self.account.address)
        tx_data["gasPrice"] = self.web3.eth.gas_price
        tx_data["value"] = int(tx_data["value"])
        #tx_data["gas"] = int(tx_data.get("gas", 250000))  # Default fallback
        tx_data["gas"] = self.estimate_gas()

        signed_tx = self.account.sign_transaction(tx_data)
        print("Transaction data:")
        print(json.dumps(tx_data, indent=4))
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return self.web3.to_hex(tx_hash)

    def estimate_gas(self):
        # Estimate gas (important!)
        try:
            estimated_gas = self.web3.eth.estimate_gas({
                "from": tx_data["from"],
                "to": tx_data["to"],
                "value": tx_data.get("value", 0),
                "data": tx_data["data"]
            })
            tx_data["gas"] = int(estimated_gas * 1.2)  # add 20% buffer
        except Exception as e:
            print(f"Gas estimation failed: {e}")
            return None


# 🔁 Example usage
if __name__ == "__main__":

    # Create client for Polygon
    client = OneInchClient(chain_id=POLYGON, private_key=K1inch.PRIVATE_KEY, api_key=K1inch.API_KEY)

    # Swap MATIC to USDC
    from_symbol = "MATIC"
    to_symbol = "USDC"
    amount_matic = 1

    from_token = client.get_token_address(from_symbol)
    to_token = client.get_token_address(to_symbol)
    amount_wei = Web3.to_wei(amount_matic, 'ether')

    quote = client.get_quote(from_token, to_token, amount_wei)
    print("Quote received:")
    print(quote)

    tx_data = client.build_swap_tx(from_token, to_token, amount_wei)


    tx_hash = client.send_transaction(tx_data)
    print(f"Transaction sent! Hash: {tx_hash}")





