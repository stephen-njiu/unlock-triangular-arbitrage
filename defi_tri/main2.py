# Import necessary libraries
import get_pairs
import func_triangular_arb
import json
import time

# Authorization
graph_api_key = 'your api key'
url = 'https://gateway.thegraph.com/api/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV'
headers = {
  'Authorization': f'Bearer {graph_api_key}',
}

# start_tokens = ["WETH", "USDC", "DAI", "USDT", "WBTC", "FRAX"]
# start_tokens = ["USDC", "USDT"]

# GraphQL query to fetch pools with specific tokens
query = """
    {
    pools(
        first: 1000,
        orderBy: totalValueLockedETH
        orderDirection: desc
        where: { token0_: { symbol_in: ["WETH", "USDC", "DAI", "USDT", "WBTC", "FRAX"] } }
    ) {
        id
        feeTier
        liquidity
        totalValueLockedETH
        totalValueLockedUSD
        token0Price
        token1Price
        token0 { id symbol name decimals totalValueLockedUSD }
        token1 { id symbol name decimals totalValueLockedUSD }
    }
    }
"""

if __name__== "__main__":
    while True:
        print("Fetching data from The Graph API...")
        pairs = get_pairs.get_initial_data(url, query, headers)
        structured_pairs = func_triangular_arb.structure_trading_pairs(pairs, limit=1000)
        print("Processing trading pairs...")
         # Get surface rates
        surface_rates_list = []
        for t_pair in structured_pairs:
            surface_rate = func_triangular_arb.calc_triangular_arb_surface_rate(t_pair, min_rate=1.5)
            if len(surface_rate) > 0:
                surface_rates_list.append(surface_rate)

        # Save to JSON file
        if len(surface_rates_list) > 0:
            with open("uniswap_surface_rates.json", "w") as fp:
                json.dump(surface_rates_list, fp)
                print("File saved.")
        print("Len of surface rates list:", len(surface_rates_list))
        time.sleep(300)
