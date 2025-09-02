const { ethers } = require("ethers");
const fs = require("fs");
const QuoterABI = require("@uniswap/v3-periphery/artifacts/contracts/lens/Quoter.sol/Quoter.json").abi;

// ----------------- CONFIG -----------------
const INFURA_URL = "https://mainnet.infura.io/v3/9833ceb4e7c54187bbf769eae0ed1533";
const provider = new ethers.providers.JsonRpcProvider(INFURA_URL);
const QUOTER_ADDRESS = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6";

// ----------------- UTILS -----------------
function getFile(path) {
  try {
    return fs.readFileSync(path, "utf8");
  } catch (err) {
    console.error("Error reading file:", err.message);
    return "[]";
  }
}

async function getTokenInfo(tokenAddress) {
  const ABI = [
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function decimals() view returns (uint)"
  ];
  const contract = new ethers.Contract(tokenAddress, ABI, provider);

  try {
    const [symbol, name, decimals] = await Promise.all([
      contract.symbol(),
      contract.name(),
      contract.decimals(),
    ]);
    return { tokenAddress, symbol, name, decimals };
  } catch (err) {
    console.warn(`⚠️  Skipping token ${tokenAddress}, metadata fetch failed: ${err.reason || err.message}`);
    return null; // tell caller to skip
  }
}

// ----------------- CORE -----------------
async function getPrice(poolAddress, amtIn, tradeDirection) {
  const poolABI = [
    "function token0() external view returns (address)",
    "function token1() external view returns (address)",
    "function fee() external view returns (uint24)",
  ];
  const pool = new ethers.Contract(poolAddress, poolABI, provider);

  try {
    const [token0, token1, fee] = await Promise.all([
      pool.token0(),
      pool.token1(),
      pool.fee(),
    ]);

    const token0Info = await getTokenInfo(token0);
    const token1Info = await getTokenInfo(token1);
    if (!token0Info || !token1Info) return 0; // skip if metadata missing

    let inputToken, outputToken, inputDecimals, outputDecimals;
    if (tradeDirection === "baseToQuote") {
      inputToken = token0Info.tokenAddress;
      inputDecimals = token0Info.decimals;
      outputToken = token1Info.tokenAddress;
      outputDecimals = token1Info.decimals;
    } else {
      inputToken = token1Info.tokenAddress;
      inputDecimals = token1Info.decimals;
      outputToken = token0Info.tokenAddress;
      outputDecimals = token0Info.decimals;
    }

    // Ensure numbers are safe
    const cleanAmtIn = typeof amtIn === "string" ? amtIn : String(amtIn);
    const amountIn = ethers.utils.parseUnits(cleanAmtIn, inputDecimals);

    const quoter = new ethers.Contract(QUOTER_ADDRESS, QuoterABI, provider);
    const quotedAmountOut = await quoter.callStatic.quoteExactInputSingle(
      inputToken,
      outputToken,
      fee,
      amountIn,
      0
    );

    return parseFloat(ethers.utils.formatUnits(quotedAmountOut, outputDecimals));
  } catch (err) {
    console.error(`Quote failed for pool ${poolAddress}, ${token0Info, token1Info, tradeDirection}:`, err.reason || err.message);
    return 0;
  }
}

function calculateArbitrage(amountIn, finalOut, surfaceObj) {
  const profitLoss = finalOut - amountIn;
  if (profitLoss <= 0) return;

  const profitLossPerc = (profitLoss / amountIn) * 100;
  console.log("\n✅ Profitable arbitrage:", {
    trade: surfaceObj,
    start: amountIn,
    end: finalOut,
    profit: profitLoss,
    profitPerc: profitLossPerc.toFixed(2) + "%",
  });
}

// ----------------- MAIN -----------------
async function getDepth(amountIn) {
  console.log("Reading surface opportunities...");
  const fileInfo = getFile("../uniswap_surface_rates.json");
  const opportunities = JSON.parse(fileInfo);

  let idx = 0;
  for (const opp of opportunities) {
    const {
      poolContract1, poolContract2, poolContract3,
      poolDirectionTrade1, poolDirectionTrade2, poolDirectionTrade3
    } = opp;
    idx += 1;

    console.log(`Simulating trade path: ${idx}`);

    const acquired1 = await getPrice(poolContract1, amountIn, poolDirectionTrade1);
    if (acquired1 === 0) continue;

    const acquired2 = await getPrice(poolContract2, acquired1, poolDirectionTrade2);
    if (acquired2 === 0) continue;

    const acquired3 = await getPrice(poolContract3, acquired2, poolDirectionTrade3);
    if (acquired3 === 0) continue;

    calculateArbitrage(amountIn, acquired3, opp);
  }
}

getDepth(100);
