import requests

from hack import K1inch

# === Configuration ===
ETH_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"  # ETH (native)
USDT_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT


def get_eth_to_usdt_spot_price():
    url = f"https://api.1inch.dev/price/v1.1/1/{ETH_ADDRESS},{USDT_ADDRESS}"

    headers = {
        "Authorization": f"Bearer {K1inch.API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        prices = response.json()
        print(prices)

        # Convert to lowercase to match JSON keys
        eth_key = ETH_ADDRESS.lower()
        usdt_key = USDT_ADDRESS.lower()

        eth_price_in_usdt = int(prices[eth_key]) / int(prices[usdt_key])
        print(f"1 ETH ≈ {eth_price_in_usdt:.6f} USDT (Spot Price)")
    else:
        print(f"Error {response.status_code}: {response.text}")


# Run it
if __name__ == "__main__":
    get_eth_to_usdt_spot_price()
