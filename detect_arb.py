import json

from hliq import get_current_funding, sort_by_value_desc
from kinch_get import get_pair
from kinch_token_list import fetch_tokens



if __name__ == "__main__":
    token = "ETH"
    tks = fetch_tokens()
    tk_1 = tks[token]
    tk_2 = tks["USDT"]
    price_usdt = get_pair(tk_1, tk_2)

    rate = get_current_funding()
    token_rate = rate[token]

    print(price_usdt)
    print(json.dumps(token_rate, indent=4))
    # rate = sort_by_value_desc(rate)
    # print(json.dumps(rate, indent=2))







