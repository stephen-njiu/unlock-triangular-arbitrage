# Unlock Triangular Arbitrage

A small proof-of-concept project for **triangular arbitrage** in crypto. Started with Poloniex (CEX), then moved to DeFi using **Uniswap V3**, querying via **The Graph** (GraphQL) and using **Infura** as the Ethereum RPC provider.

---

## What It Does

- Scans for 3-token arbitrage cycles (A → B → C → A)  
- Uses on-chain data (Uniswap V3) to compute prices and liquidity  
- Detects if there's a net profit after considering fees and slippage  

---

## How Triangular Arbitrage Works

1. You pick a starting token, **A**.  
2. You swap **A → B**, then **B → C**, then **C → A**.  
3. If the final amount of **A** is greater than what you started with (after fees and slippage), there is an arbitrage opportunity.  
4. The engine builds all possible 3-token paths, fetches real-time pool data, simulates the trades, and flags profitable cycles.

---

## Disclaimer

This project is **for educational and research purposes only**. Running arbitrage in real markets carries significant risk: transaction costs, slippage, latency, and MEV can make strategies unprofitable or even loss-making. Use at your own risk.  

---

## License & Contact

Feel free to explore, fork, or build on this code. If you have questions or ideas, welcome to open an issue or reach out.

