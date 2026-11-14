<div align="center">

# Karachi Stock Simulator

**A C++ Windows console simulator for trading a 12-company mock market in Pakistani rupees.**

[![Language](https://img.shields.io/badge/Language-C%2B%2B-12675A?style=for-the-badge&logo=cplusplus&logoColor=white)](#project-breakdown)
[![Platform](https://img.shields.io/badge/Platform-Windows-2C5863?style=for-the-badge&logo=windowsterminal&logoColor=white)](#setup)
[![Data](https://img.shields.io/badge/Data-12%20companies-446034?style=for-the-badge)](data/companies.csv)
[![Gallery](https://img.shields.io/badge/Gallery-24%20figures-365E83?style=for-the-badge)](#gallery)
[![Build](https://img.shields.io/badge/Build-CMake-243D68?style=for-the-badge&logo=cmake&logoColor=white)](CMakeLists.txt)
[![Demo](https://img.shields.io/badge/Demo-Walkthrough-74501D?style=for-the-badge&logo=github&logoColor=white)](#recruiter-demo)
[![Export](https://img.shields.io/badge/Export-CSV-175653?style=for-the-badge&logo=microsoftexcel&logoColor=white)](#project-breakdown)
[![Checks](https://img.shields.io/badge/Checks-Smoke%20test-5B417B?style=for-the-badge&logo=python&logoColor=white)](tests/smoke_test.py)

</div>

## Live Links

| What | Link |
|---|---|
| Repository | [https://github.com/rohaan2802/KarachiStockMarket_PF](https://github.com/rohaan2802/KarachiStockMarket_PF) |
| GitHub Pages | [https://rohaan2802.github.io/Karachi_Stock_Simulator/](https://rohaan2802.github.io/Karachi_Stock_Simulator/) |
| Original assignment brief | [https://github.com/rohaan2802/KarachiStockMarket_PF/blob/1c8fdd524bdc24df7a0cf8496fdc51977b39e7ea/docs/Project.pdf](https://github.com/rohaan2802/KarachiStockMarket_PF/blob/1c8fdd524bdc24df7a0cf8496fdc51977b39e7ea/docs/Project.pdf) |

## Contents

- [Live Links](#live-links)
- [Overview](#overview)
- [What's Inside](#whats-inside)
- [Recruiter Demo](#recruiter-demo)
- [Project Breakdown](#project-breakdown)
- [Folder Structure](#folder-structure)
- [Setup](#setup)
- [Results](#results)
- [Limitations](#limitations)
- [Gallery](#gallery)
- [About the Author](#about-the-author)

## Overview

Karachi Stock Simulator is a Windows console project by Mohammad Rohaan for Programming Fundamentals at FAST-NUCES. It models a local stock market and a personal portfolio using a bundled snapshot of 12 listed companies. The program generates mock prices locally in Pakistani rupees.

## What's Inside

| Component | Purpose |
|---|---|
| [C++ simulator](src/market_simulator.cpp) | Complete application with market, ranking, export and portfolio views |
| [CMake project](CMakeLists.txt) | Build target and Visual Studio debugger configuration |
| [Technical walkthrough](docs/technical_walkthrough.md) | Architecture, data contracts and a recruiter demo script |
| [Company data](data/companies.csv) | Headerless symbol, company name and starting price rows |
| [Assignment brief](docs/project_brief.pdf) | Original course requirements |
| [Self-evaluation](docs/self_evaluation.pdf) | Original feature checklist |
| [Console display notes](docs/console_display_notes.pdf) | Earlier Windows console troubleshooting |
| [Saved sample](docs/portfolio_sample.txt) | Example portfolio text report |
| [Smoke test](tests/smoke_test.py) | Runs the built program with isolated inputs and checks its saved files |

## Recruiter Demo

| Step | Action | What to inspect |
|---|---|---|
| 1 | Launch with **run.bat** and press **Enter** | Previous price, current price, and the session high and low |
| 2 | Press **S** | The same companies sorted by percentage return from their opening prices |
| 3 | Press **X** | A spreadsheet-friendly snapshot in **session/market_snapshot.csv** |
| 4 | Open **P**, deposit cash with **M**, and buy two **PSO** shares with **A** | Cash decreases and the portfolio shows the open position |
| 5 | Sell one share with **R**, exit with **E**, and reopen the portfolio | One share and the resulting cash balance persist |

The [technical walkthrough](docs/technical_walkthrough.md) connects those screens to their C++ functions and explains the exported columns.

## Project Breakdown

At startup the app loads a plain CSV, rejects malformed or duplicate entries, and fixes each stock’s opening price for that session. A refresh applies a randomized whole-rupee and fractional change, rounds to cents, clamps to the nearest allowed cent inside the ±15% band, and updates previous, high and low prices. The market board also shows the top percentage movers and the number of shares bought and sold in the session.

The session ranking sorts by return from the opening quote. The Live Market footer compares the current tick with the previous tick, so the two views can highlight different companies. Exporting writes a point-in-time CSV with opening, previous, current, high, low and return-from-open columns.

The portfolio uses dynamically resized arrays for symbols and share counts. Buying debits cash at the current simulated price. Selling credits cash and removes fully sold positions. Portfolio gain or loss compares current and previous tick values for shares still held. Cash and holdings are saved in a readable text report. The original report format remains readable by the application.

| Key | Action |
|---|---|
| Enter | Refresh every stock |
| P / L | Open Portfolio / return to Live Market |
| M / W | Deposit cash / withdraw cash (Portfolio only) |
| A / R | Buy / sell by stock symbol |
| S / X | Rank stocks by return from open / export the current market snapshot |
| E | Exit and save |

## Folder Structure

```text
Karachi_Stock_Simulator/
├── src/           Windows C++ simulator
├── data/          Tracked seed prices
├── docs/          Assignment, sample, display notes and archive
├── tests/         Executable smoke test
├── assets/        Site CSS, JavaScript, captures and previews
├── CMakeLists.txt C++17 build and IDE project
├── index.html     GitHub Pages entry point
├── build.bat      Compile using MSVC or MinGW-w64
└── run.bat        Build and start a local session
```

[Archive notes](docs/archive/README.md) identify the earlier versions and the original files.

## Setup

On Windows, install the MSVC C++ Build Tools or place MinGW-w64 C++ on PATH. From the project folder, run:

```powershell
.\run.bat
```

Open **P** to create a portfolio and enter an owner name. Deposit **10,000** with **M**, buy **2 PSO** shares with **A**, and refresh the board with **Enter**. Try selling one share with **R** and exit with **E**. On the next run choose **P → 1** to resume. For a fresh start, close the simulator and remove the local **session/** folder. The launcher copies the bundled seed to that folder and the program writes current prices and portfolio state there.

For IDE review, open the repository folder as a CMake project in Visual Studio. The CMake target builds the same C++ source and puts a seed copy in the build directory’s session folder. For a command-line build:

```powershell
cmake -S . -B build/ide
cmake --build build/ide --config Debug
```

To run the executable-based verification suite with Python 3:

```powershell
.\build.bat
python tests/smoke_test.py
```

## Results

The [saved portfolio sample](docs/portfolio_sample.txt) illustrates the block report, including owner, cash, per-symbol prices, share count, and totals. A normal local run writes updated quotes to **session/companies.txt** and creates **session/portfolio.txt** when a portfolio is set up. Closing an untouched session preserves any existing portfolio file. Local checks passed for the C++ build, 500 refreshes with prices inside their session bounds, deposits, withdrawals, buys, sells, rejection paths persistence, ranking order, and CSV calculation accuracy. The gallery was also checked at mobile, tablet and desktop widths in light and dark themes. Figures label their sources so readers can distinguish saved examples, source inspection, assignment excerpts and captured output.

## Limitations

Prices come from a classroom snapshot and simulated random ticks. The console targets Windows and uses Win32 display APIs. The app supports one local portfolio and up to 50 company rows. The saved files are independent and the simulator expects one running instance per session folder. There are no fees, order book, real-time quotes, or cost-basis returns.

## Gallery

### Live Market board

<p align="left"><a href="assets/screenshots/08-live-market-board-sage.png"><img src="assets/thumbs/08-live-market-board-sage.webp" width="960" alt="Live Market board"></a></p>

Output from running the Windows simulator with the bundled quotes.

### Session ranking

<p align="left"><a href="assets/screenshots/07-session-ranking-sage.png"><img src="assets/thumbs/07-session-ranking-sage.webp" width="960" alt="Session ranking"></a></p>

Companies sorted by percentage return from their opening quote.

### Exported market snapshot

<p align="left"><a href="assets/screenshots/19-exported-market-snapshot-sage.png"><img src="assets/thumbs/19-exported-market-snapshot-sage.webp" width="960" alt="Exported market snapshot"></a></p>

Selected columns from the CSV written during a smoke-test run.

### Company snapshot

<p align="left"><a href="assets/screenshots/01-company-snapshot-sage.png"><img src="assets/thumbs/01-company-snapshot-sage.webp" width="960" alt="Company snapshot"></a></p>

Twelve bundled symbol, company and starting price records.

### Market input validation

<p align="left"><a href="assets/screenshots/02-market-input-validation-sage.png"><img src="assets/thumbs/02-market-input-validation-sage.webp" width="960" alt="Market input validation"></a></p>

The CSV parser validates names, prices and duplicate symbols.

### Stock symbol lookup

<p align="left"><a href="assets/screenshots/03-stock-symbol-lookup-sage.png"><img src="assets/thumbs/03-stock-symbol-lookup-sage.webp" width="960" alt="Stock symbol lookup"></a></p>

Linear search matches symbols regardless of letter case.

### Random tick generation

<p align="left"><a href="assets/screenshots/04-random-tick-generation-sage.png"><img src="assets/thumbs/04-random-tick-generation-sage.webp" width="960" alt="Random tick generation"></a></p>

The refresh combines a whole-number delta and a fractional delta.

### The session price band

<p align="left"><a href="assets/screenshots/05-the-session-price-band-sage.png"><img src="assets/thumbs/05-the-session-price-band-sage.webp" width="960" alt="The session price band"></a></p>

Cent rounding stays inside the opening price’s ±15% limits.

### Highs, lows and tick change

<p align="left"><a href="assets/screenshots/06-highs-lows-and-tick-change-sage.png"><img src="assets/thumbs/06-highs-lows-and-tick-change-sage.webp" width="960" alt="Highs, lows and tick change"></a></p>

Each price refresh updates session extremes and the percentage move.

### Holdings allocation

<p align="left"><a href="assets/screenshots/09-holdings-allocation-sage.png"><img src="assets/thumbs/09-holdings-allocation-sage.webp" width="960" alt="Holdings allocation"></a></p>

The holdings arrays grow as new symbols enter the portfolio.

### Portfolio valuation

<p align="left"><a href="assets/screenshots/10-portfolio-valuation-sage.png"><img src="assets/thumbs/10-portfolio-valuation-sage.webp" width="960" alt="Portfolio valuation"></a></p>

The totals function marks held shares at previous and current prices.

### Portfolio setup

<p align="left"><a href="assets/screenshots/11-portfolio-setup-sage.png"><img src="assets/thumbs/11-portfolio-setup-sage.webp" width="960" alt="Portfolio setup"></a></p>

The console creates a named portfolio when no saved file exists.

### Continuing a portfolio

<p align="left"><a href="assets/screenshots/12-continuing-a-portfolio-sage.png"><img src="assets/thumbs/12-continuing-a-portfolio-sage.webp" width="960" alt="Continuing a portfolio"></a></p>

The startup menu offers a saved portfolio, a fresh portfolio, or cancel.

### Trade and cash confirmations

<p align="left"><a href="assets/screenshots/13-trade-and-cash-confirmations-sage.png"><img src="assets/thumbs/13-trade-and-cash-confirmations-sage.webp" width="960" alt="Trade and cash confirmations"></a></p>

The simulator confirms the deposit, buy, sell and withdrawal.

### Withdrawal flow

<p align="left"><a href="assets/screenshots/14-withdrawal-flow-sage.png"><img src="assets/thumbs/14-withdrawal-flow-sage.webp" width="960" alt="Withdrawal flow"></a></p>

The prompt accepts a rupee amount or zero to cancel the operation.

### Rejected buy orders

<p align="left"><a href="assets/screenshots/15-rejected-buy-orders-sage.png"><img src="assets/thumbs/15-rejected-buy-orders-sage.webp" width="960" alt="Rejected buy orders"></a></p>

The simulator rejects an unknown symbol and an order exceeding available cash.

### Sell order entry

<p align="left"><a href="assets/screenshots/16-sell-order-entry-sage.png"><img src="assets/thumbs/16-sell-order-entry-sage.webp" width="960" alt="Sell order entry"></a></p>

A sell is handled against the same quote arrays and the investor’s holdings.

### Saved PSO position

<p align="left"><a href="assets/screenshots/17-saved-pso-position-sage.png"><img src="assets/thumbs/17-saved-pso-position-sage.webp" width="960" alt="Saved PSO position"></a></p>

The generated portfolio report records the remaining PSO share and cash.

### Saved portfolio totals

<p align="left"><a href="assets/screenshots/18-saved-portfolio-totals-sage.png"><img src="assets/thumbs/18-saved-portfolio-totals-sage.webp" width="960" alt="Saved portfolio totals"></a></p>

Report footer produced after a deposit, buy, sell and withdrawal.

### Session exit

<p align="left"><a href="assets/screenshots/20-session-exit-sage.png"><img src="assets/thumbs/20-session-exit-sage.webp" width="960" alt="Session exit"></a></p>

Exit writes the market and writes the portfolio when it was opened or changed.

### Ranking sort logic

<p align="left"><a href="assets/screenshots/21-ranking-sort-logic-sage.png"><img src="assets/thumbs/21-ranking-sort-logic-sage.webp" width="960" alt="Ranking sort logic"></a></p>

Stable sorting orders symbols by return from their opening quote.

### CSV export logic

<p align="left"><a href="assets/screenshots/22-csv-export-logic-sage.png"><img src="assets/thumbs/22-csv-export-logic-sage.webp" width="960" alt="CSV export logic"></a></p>

The export writes quotes and percentage returns, then replaces the previous snapshot.

### Bounds verification

<p align="left"><a href="assets/screenshots/23-bounds-verification-sage.png"><img src="assets/thumbs/23-bounds-verification-sage.webp" width="960" alt="Bounds verification"></a></p>

The smoke test refreshes the real program 500 times and checks saved quotes.

### Portfolio regression checks

<p align="left"><a href="assets/screenshots/24-portfolio-regression-checks-sage.png"><img src="assets/thumbs/24-portfolio-regression-checks-sage.webp" width="960" alt="Portfolio regression checks"></a></p>

The suite checks trades, quiet exit, invalid input and reopening saved holdings.


## About the Author

**Mohammad Rohaan** developed the simulator as a Programming Fundamentals final project. [GitHub profile](https://github.com/rohaan2802).
