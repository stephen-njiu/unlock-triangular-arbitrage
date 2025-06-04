import requests 
import json


def get_prices(url):
    req = requests.get(url)
    coin_json = json.loads(req.text)
    prices_dict = {entry['symbol']: entry for entry in coin_json}
    return prices_dict

def get_tradeables(url):
    req = requests.get(url)
    coin_json = json.loads(req.text)
    coin_list = []
    for pair in coin_json:
        coin_list.append(pair['symbol'])
    return coin_list

## Getting the arbitrage tradeable pairs
# 1. Start from A
# 2. Go through all coins
# 3. Find B pair where one coin matched
# 4. Find C pair where base and quote exist in A and B configurations

def get_triangular_pairs(coin_list, num_of_pairs=100):
    triangular_pairs_list = []
    remove_duplicates_list = []
    pairs_list = coin_list[0:num_of_pairs]

    # Get pair A
    for pair_a in pairs_list:
        pair_a_split = pair_a.split("_")
        a_base = pair_a_split[0]
        a_quote = pair_a_split[1]

        # assign a to a box
        a_pair_box = [a_base, a_quote]

    # Get pair B
        for pair_b in pairs_list:
            pair_b_split = pair_b.split("_")
            b_base = pair_b_split[0]
            b_quote = pair_b_split[1]

            # check pair B

            if pair_b != pair_a:
                if b_base in a_pair_box or b_quote in a_pair_box:
                    # Get pair c
                    for pair_c in pairs_list:
                        pair_c_split = pair_c.split("_")
                        c_base = pair_c_split[0]
                        c_quote =pair_c_split[1] 

                        # count the number of matching items
                        if pair_c != pair_a and pair_c != pair_b:
                            combine_all = [pair_a, pair_b, pair_c]
                            pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]

                            counts_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    counts_c_base += 1
                            
                            counts_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    counts_c_quote += 1
                            

                            # Determining Triangular Match
                            if counts_c_base == 2 and counts_c_quote == 2 and c_base != c_quote:
                                # print(pair_a, pair_b, pair_c)
                                combined = pair_a + "," + pair_b + "," + pair_c
                                unique_item = ''.join(sorted(combine_all))
                                if unique_item not in remove_duplicates_list:
                                    match_dict = {
                                        "a_base":a_base,
                                        "b_base":b_base,
                                        "c_base":c_base,
                                        "a_quote":a_quote,
                                        "b_quote":b_quote,
                                        "c_quote":c_quote,
                                        "pair_a":pair_a,
                                        "pair_b":pair_b,
                                        "pair_c":pair_c,
                                        "combined":combined
                                    }
                                    triangular_pairs_list.append(match_dict)
                                    remove_duplicates_list.append(unique_item)

    # print(len(triangular_pairs_list))
    return triangular_pairs_list
    # print(triangular_pairs_list[0:20])



def get_price_for_t_pair(t_pair, prices_json):
    # extract pair info
    pair_a = t_pair["pair_a"]
    pair_b = t_pair["pair_b"]
    pair_c = t_pair["pair_c"]
    # Extract price information
    pair_a_ask = float(prices_json[pair_a]['ask'])
    pair_a_bid = float(prices_json[pair_a]['bid'])
    pair_b_ask = float(prices_json[pair_b]['ask'])
    pair_b_bid = float(prices_json[pair_b]['bid'])
    pair_c_ask = float(prices_json[pair_c]['ask'])
    pair_c_bid = float(prices_json[pair_c]['bid']) 
    # print(pair_a, pair_a_ask, pair_a_bid)
    return {
        "pair_a_ask":pair_a_ask,
        "pair_a_bid":pair_a_bid,
        "pair_b_ask":pair_b_ask,
        "pair_b_bid":pair_b_bid,
        "pair_c_ask":pair_c_ask,
        "pair_c_bid":pair_c_bid,
    }


# calculation of of Surface Rates

def calculate_surface_rate(t_pair, prices_dict):
    # Set Variables
    starting_amount = 1
    min_surface_rate = 0
    surface_dict = {}
    contract_2 = ""
    contract_3 = ""
    direction_trade_1 = ""
    direction_trade_2 = ""
    direction_trade_3 = ""
    acquired_coin_t2 = 0
    acquired_coin_t3 = 0
    calculated = 0

    # Extract Pair Variables
    a_base = t_pair["a_base"]
    a_quote = t_pair["a_quote"]
    b_base = t_pair["b_base"]
    b_quote = t_pair["b_quote"]
    c_base = t_pair["c_base"]
    c_quote = t_pair["c_quote"]
    pair_a = t_pair["pair_a"]
    pair_b = t_pair["pair_b"]
    pair_c = t_pair["pair_c"]

    # Extract Price Information
    a_ask = prices_dict["pair_a_ask"]
    a_bid = prices_dict["pair_a_bid"]
    b_ask = prices_dict["pair_b_ask"]
    b_bid = prices_dict["pair_b_bid"]
    c_ask = prices_dict["pair_c_ask"]
    c_bid = prices_dict["pair_c_bid"]
