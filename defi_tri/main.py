# Import necessary libraries
import get_pairs
import get_cycles
import surface_rate
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
        first: 3000,
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
        pairs_dict = get_pairs.get_initial_data(url, query, headers)
        print("Processing trading pairs...")
        all_pairs = get_pairs.trading_pairs(pairs_dict) # we are getting all pairs here
        filtered_pairs = get_pairs.get_liquidity_pairs(all_pairs)
        print("Identifying triangular arbitrage cycles...")
        triangle_cycles = get_cycles.triangular_cycles(filtered_pairs, limit=2000)# maximum = 2000

        all_surface_rate = []
        for cycle in triangle_cycles:
            arb_rates = surface_rate.calculate_surface_arb(cycle, start_amount=1, min_surface_rate=1.2) # min_rate is in percentage
            if arb_rates:
                all_surface_rate.append(arb_rates)
        if len(all_surface_rate) > 0:
            with open("uniswap_surface_rates.json", "w") as fp:
                json.dump(all_surface_rate, fp, indent=2)
                print(f"Surface rates saved to uniswap_surface_rates.json, {len(all_surface_rate)} arbitrage opportunities found.")

        time.sleep(300) # wait for 5 minutes before fetching new data

