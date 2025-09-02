import requests

def get_initial_data(url, query, headers):
    try:
        req = requests.post(url, json={'query': query}, headers=headers)
    except Exception as e:
        print(f"Error fetching data from The Graph API: {e}")
    json_data = req.json()
    pairs_dict = json_data['data']['pools']
    return pairs_dict

def trading_pairs(pairs_dict):
    pairs = []
    for pair in pairs_dict:
        pair_info = {
            'id': pair['id'],
            'feeTier': int(pair['feeTier']),
            'liquidity': float(pair['liquidity']),
            'totalValueLockedETH': float(pair['totalValueLockedETH']),
            'totalValueLockedUSD': float(pair['totalValueLockedUSD']),
            'pair': pair['token0']['symbol'] + '_' + pair['token1']['symbol'],
            'token0': {
                'id': pair['token0']['id'],
                'symbol': pair['token0']['symbol'],
                'name': pair['token0']['name'],
                'decimals': int(pair['token0']['decimals']),
                'totalValueLockedUSD': float(pair['token0']['totalValueLockedUSD'])
            },
            'token1': {
                'id': pair['token1']['id'],
                'symbol': pair['token1']['symbol'],
                'name': pair['token1']['name'],
                'decimals': int(pair['token1']['decimals']),
                'totalValueLockedUSD': float(pair['token1']['totalValueLockedUSD'])
            },
            'token0Price': float(pair['token0Price']),
            'token1Price': float(pair['token1Price'])
        }
        pairs.append(pair_info)
    return pairs


def get_liquidity_pairs(all_pairs): # only pairs with liquidity > 1000 and totalValueLockedUSD > 1000
    filtered_pairs = []
    # just_pairs = []
    for pair in all_pairs:
        if (
            pair['liquidity'] > 1000
            and pair['totalValueLockedUSD'] > 1000
            and (pair['token0']['totalValueLockedUSD'] > 1000 or pair['token1']['totalValueLockedUSD'] > 1000)
        ):
            filtered_pairs.append(pair)
            # just_pairs.append(pair['pair'])

    return filtered_pairs#, just_pairs
