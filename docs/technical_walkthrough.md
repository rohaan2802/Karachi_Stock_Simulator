# Technical walkthrough

## Architecture

The executable in [src/market_simulator.cpp](../src/market_simulator.cpp) uses C++17 and the Windows console API. Open the repository in Visual Studio as a [CMake project](../CMakeLists.txt), or start with the [Windows launcher](../run.bat).

| Area | Entry points | Responsibility |
|---|---|---|
| Startup | `main`, `loadCompanies` | Load up to 50 unique symbols into parallel market arrays and initialize opening, previous, current, high and low prices. |
| Quote updates | `refreshAllPrices` | Generate ticks in rupees and cents, clamp them within ±15% of the opening quote, then update the tick and session statistics. |
| Market analysis | `showMarketRanking`, `openingReturn` | Sort indices by return from open while preserving the original quote order. Equal returns retain the input order. |
| Market export | `exportMarketSnapshot` | Write the current quote values to a temporary CSV and replace the prior export after a successful write. |
| Portfolio | `addStock`, `removeStock`, `computePortfolioTotals` | Validate available cash or shares, update positions and calculate the portfolio value from current quotes. |
| Persistence | `saveCompanies`, `loadPortfolio`, `savePortfolio` | Carry the final quotes and portfolio state between runs. |

## Input and outputs

[The seed CSV](../data/companies.csv) contains one record per company in symbol, company name and price order. The launcher copies it to an ignored local session folder. A saved quote file becomes the starting point for later sessions. Every restart establishes a new opening price band.

| File | Produced by | Fields and behavior |
|---|---|---|
| `session/companies.txt` | Exit | Symbol, company name and final quoted price. This becomes the next session's market input. |
| `session/portfolio.txt` | Portfolio setup, successful actions and exit | Owner, cash, held symbols and quantities, and a readable valuation summary. |
| `session/market_snapshot.csv` | X in either console view | Symbol, opening quote, previous quote, current quote, high, low and return from open. Prices use two decimal places and return uses four. Each export replaces the previous snapshot. |

To reproduce an exported return, subtract the opening quote from the current quote, divide by the opening quote and multiply by 100. The ranking uses the same calculation. The footer on the market board uses the last tick instead, with the previous quote as its denominator. A rank can move even if the last tick and the return from open have different signs.

## Five-minute demo

1. Start with `run.bat`. Press Enter twice and point out which prices changed and how the high and low columns track the session.
2. Press S and compare the first and last rows. Press any key to return, press X, and open the export in a spreadsheet.
3. Press P to create a portfolio. Deposit Rs. 10,000 with M, buy two PSO shares with A, and refresh the market.
4. Sell one PSO share with R, withdraw Rs. 100 with W, and inspect the remaining holding and the cash total.
5. Exit with E. Restart and use P then 1 to load the saved portfolio. The [smoke test](../tests/smoke_test.py) exercises these paths with isolated working files and independently checks ranking order and the exported return calculations.

The app is a single-user classroom simulation with locally generated ticks. The app uses one working directory per session. The starter and prior portfolio files are in the [archive](archive/README.md).
