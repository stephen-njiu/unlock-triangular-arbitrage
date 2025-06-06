import json
import time
import func_arbitrage

url = 'https://api.poloniex.com/markets/ticker24h'

def step_0():
    coin_list = func_arbitrage.get_tradeables(url)
    return coin_list
    # print(coin_list)
    # print(len(coin_list))

def step_1(coin_list, num_of_pairs=500):
    triangular_pairs = func_arbitrage.get_triangular_pairs(coin_list=coin_list, num_of_pairs=num_of_pairs)
    print(triangular_pairs)
    # save to a json file
    with open("structured_pairs.json","w") as f:
        json.dump(triangular_pairs, f)

def step_2():
    # get json tradeable triangular pairs
    with open("structured_pairs.json") as json_file:
        structured_pairs = json.load(json_file)
    
    # get latest prices.
    prices_json = func_arbitrage.get_prices(url=url)
    # print(prices_json)
    for pair in structured_pairs:
        time.sleep(0.3)
        prices_dict = func_arbitrage.get_price_for_t_pair(t_pair=pair, prices_json=prices_json)
        surface_arb = func_arbitrage.calculate_surface_rate(pair, prices_dict)
        # print(surface_arb)

        if len(surface_arb) > 0:
            real_rate_arb = func_arbitrage.get_depth_from_orderbook(surface_arb)
            print(real_rate_arb)
            time.sleep(20)



if __name__ == '__main__':
    # coin_list = step_0()
    # step_1(coin_list=coin_list)
    step_2()