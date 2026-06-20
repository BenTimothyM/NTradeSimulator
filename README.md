# NTrade Simulator (Professional Retro-Cyber Financial Dashboard & Game Engine)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.0-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Rich UI](https://img.shields.io/badge/UI-Rich_Terminal-magenta?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

**NTrade Simulator** is a robust, command-line interface (CLI) financial simulation platform built with a distinct retro-cyber terminal aesthetic. The project seamlessly integrates deep market trading operations (Cryptocurrencies, Stocks, and Forex) with an advanced game loop simulating macroeconomics, debt risk management, yield farming, and recurring financial liabilities.

> **🌱 Learning Playground:**
> This repository serves as an advanced sandbox for Object-Oriented Programming (OOP) in Python, persistent database state tracking (SQLite3), mathematical financial modeling (geometric random walks, maintenance margin limits, debt enforcement ratios), and highly structured interactive terminal UI layouts utilizing the Rich rendering framework.

---

## 📖 Project Overview

Experience the high-stakes environment of a professional proprietary trader directly from your operating system's terminal session. 

In **NTrade Simulator**, players begin their career with an initial capital of **$10,000.00**. The objective is to navigate volatile market cycles, optimize capital allocation, and climb from a humble *Broke Retailer* to a dominant *Financial Institution*. The engine enforces institutional-grade risk metrics including execution fees, maintenance margins, automated debt repossessions, and persistent account permadeath constraints.

---

## ✨ Key Features

* 🎨 **Immersive Retro-Cyber UI:** Features a beautifully structured terminal dashboard optimized with text panels, data grids, real-time status alerts, and contextual logs built entirely via the `Rich` framework.
* 🌍 **Global Multi-Asset Coverage:** Supports an extensive roster of simulated global trading pairs spanning Major Cryptocurrencies, Blue-Chip Stocks, and Forex pairs, moving far beyond standard baseline configurations.
* 🌐 **Dual-Mode Market Synchronization:** Offers toggleable access between a fully offline macroeconomic simulation engine or a live online market data stream that synchronizes true asset valuation in real-time using `yfinance` integration.
* 🛠️ **Configurable Price API Engine:** Designed with high architectural flexibility allowing custom API endpoints, parameter adjustments, and credentials for real-time live data streaming.
* 💾 **Persistent Account & State Tracking (SQLite):** Automatically writes full state snapshots—including portfolios, net worth variables, trade ledgers, and cash balances—to a local SQLite database. Features 5 distinct save slots with support for custom slot identification naming.
* 📈 **Dynamic Graphical Market Feeds:** Built-in ASCII charting engine that renders historical trend lines and real-time block indicators directly within the centralized UI interface.
* 🔌 **Algorithmic Offline Prediction Engine:** The offline mode operates via geometric random walks governed by underlying mathematical micro-trends. Price trajectories are engineered to reward logical trend calculations and technical market reads while preserving state changes seamlessly.
* ⚖️ **Bidirectional Two-Way Trading (Long & Short):** Enforces professional market flexibility by allowing standard Buy (*LONG*) or Short Sell (*SHORT*) orders, empowering players to remain profitable and extract capital gains even during severe market crashes.
* ⏱️ **Comprehensive Multi-Timeframe Historical Trackers:** Captures deep analytical histories across versatile interval parameters ranging from intra-hour frames (1m, 5m, 15m, 45m) and core hourly periods (1h, 4h, 12h) to daily, weekly, monthly, and yearly historical viewpoints.
* 🛡️ **Automated Capital Controls (Limit, TP, & SL):** Protects trading capital by maintaining an order book for pending *Limit Orders*, fully integrated with automated *Take Profit* (TP) target triggers and risk-reducing *Stop Loss* (SL) execution boundaries.
* 🚀 **Dynamic Leverage Multiples:** Amplify potential financial returns with leverage settings scaling up to **50x**. The framework provides absolute flexibility to engage or fully deactivate leverage operations based on individual risk parameters.
* 🌾 **Staking Vaults & Yield Farming:** Lock up idle cash reserves into an interest-bearing staking contract to generate passive compounding returns that accrue automatically on every simulated game tick.
* 📊 **Real-Time Market Sentiment Analysis:** Pulls live global *Fear & Greed Index* metrics directly from web feeds to evaluate macro-level psychological trends influencing market momentum.
* 📰 **Macroeconomic Wire (100 Scripted News Events):** Introduces sudden market shocks and volatility adjustments driven by **100 unique built-in news feeds** (e.g., Elon Musk tweets, technical glitch outrages, central bank interventions) to guarantee distinct non-repetitive gameplay.
* 💸 **Gas Fee & Taxation Simulation:** Enforces a realistic **0.1%** fee/tax structure across all trade executions, instructing players to accurately calculate precise net profitability metrics over raw gross gains.
* 🏆 **Progression Tier Ranks:** Features dynamic financial stratification determined by absolute evaluated Net Worth. Climb from a *Broke Retailer* up to an elite *Whale* or *Financial Institution* tier to assert dominance.
* 🏎️ **Luxury Store & Status Asset Acquisition:** Reinvest trading profits into concrete status symbols via the luxury asset inventory. Purchase Rolex watches, GT supercars, or high-end SuperYachts to significantly increase your Status Reputation Points (RP).
* 🏠 **Recurring Monthly Cost of Living (Life Expenses):** Enforces economic realism via recurring periodic cash deductions representing housing rent, food, and utilities. Running out of liquid cash triggers an emergency liquidation protocol that forces the fire-sale of open positions at market rates, regardless of losses.
* 🏦 **Bank Credit Lines & Debt Enforcement:** Access institutional bank credit lines for emergency capital injection at compounding interest rates. However, violating capital safety ratios triggers aggressive *Debt Collector* protocols that forcefully seize cash, liquidate trades, or repossess luxury assets.
* 💀 **System Hard Resets & Brutal Hardcore Mode:** Provides clear mechanisms for database clearing to start from zero, alongside a **Hardcore Mode** where dropping below zero net worth instantly initiates *Permadeath*, permanently scrubbing the save slot from the system.

---

## 💻 Tech Stack

* **Language:** Python 3.8+
* **Database Engine:** SQLite3 (Native Framework)
* **UI Rendering:** Rich Terminal Text Engine (Layouts, Panels, Custom Grids, Styled Tables)
* **Financial Data Routing:** yfinance (Yahoo Finance API), Requests

---

## 🚀 Installation & Setup

Follow these operational steps to install dependencies and deploy the financial dashboard engine locally:

### 1. Prerequisites
Ensure you have **Python 3.8 or higher** installed on your target machine (Windows, macOS, or Linux distribution). Confirm by executing:

```bash
python --version

```

### 2. Clone the Repository

Open your preferred terminal console and clone the source files:

```bash
git clone https://github.com/BenTimothyM/NTradeSimulator.git
cd NTradeSimulator

```

### 3. Set Up a Virtual Environment (Optional but Recommended)

To isolate dependencies and keep your global operating system's Python environment clean, you can initialize a local virtual environment:

* **On Windows:**

```bash
  python -m venv venv
  venv\Scripts\activate

```

* **On macOS / Linux:**

```bash
  python3 -m venv venv
  source venv/bin/activate

```

### 4. Install Third-Party Dependencies

Deploy the necessary layout libraries and real-time stock routing packages via pip:

```bash
pip install rich yfinance ccxt requests

```

### 5. Boot the Simulation Engine

Execute the core runtime entry point file to initialize the retro-cyber splash interface:

```bash
python main.py

```

---

## 💡 Operational Command Keys (Dashboard Navigation)

Input the following command flags at the `NT-Prompt>` prompt to interact with the system loop:

* **`T`** : **Tick Timeframe** — Advances the game clock, updates market logic, and recalculates passive yields/interest.
* **`B`** : **Buy / LONG** — Opens a new market or pending limit buy configuration.
* **`S`** : **Sell / SHORT** — Establishes a short position to profit off asset depreciations.
* **`C`** : **Close Position** — Manually dissolves an active trade index to realize PnL.
* **`F`** : **Yield Farming** — Accesses the staking vault dashboard interface.
* **`L`** : **Bank Loans** — Manages lines of credit, borrowing requests, or debt repayment plans.
* **`P`** : **Shop Luxury** — Opens the status asset catalogue for reputation upgrades.
* **`A`** : **Change Chart** — Switches the terminal viewport target to another ticker.
* **`K`** : **Toggle Market Mode** — Instantly shifts between offline simulation or internet live data sync.
* **`Q`** : **Quit System** — Writes an auto-save snapshot safely and exits to the home screen.

---

## 👨‍💻 Credits

This simulation engine is entirely engineered and maintained by:

* **Ben Timothy** - [@BenTimothyM](https://www.google.com/search?q=https://github.com/BenTimothyM)

## 📜 License

This financial simulation package is open-source software distributed under the official terms of the **MIT License**. Review the `LICENSE` file for deep copyright and permissions boundaries.
