import json

from hliq import get_current_funding, sort_by_value_desc
from kinch_get import get_pair
from kinch_token_list import fetch_tokens

def quote(token):
    tks = fetch_tokens()
    print(json.dumps(tks, indent=4))
    tk_1 = tks[token]
    tk_2 = tks["USDT"]
    price_usdt = get_pair(tk_1, tk_2)

    rate = get_current_funding()
    token_rate = rate[token]

    result = {}

    result["simbol"] = token
    result["market_price"] = price_usdt
    result["funding"] = token_rate["funding"]
    result["oracle_price"] = token_rate["oraclePx"]

    return result

if __name__ == "__main__":
    token = "VVV"
    qt  = quote(token)

    print(json.dumps(qt, indent=4))
    # rate = sort_by_value_desc(rate)
    # print(json.dumps(rate, indent=2))







