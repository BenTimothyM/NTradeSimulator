# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

import random
import math
import requests
import yfinance as yf
from config import ASSET_CONFIG

class MarketEngine:
    def __init__(self, online_mode=False):
        self.online_mode = online_mode
        self.prices = {ticker: data["start_price"] for ticker, data in ASSET_CONFIG.items()}
        self.price_history = {ticker: [data["start_price"]] for ticker, data in ASSET_CONFIG.items()}
        self.trends = {ticker: 0.0 for ticker in ASSET_CONFIG}
        self.api_keys = {"alpha_vantage": ""}

    def set_online_mode(self, mode: bool):
        self.online_mode = mode

    def set_api_keys(self, keys: dict):
        self.api_keys.update(keys)

    def tick(self, active_news=None):
        if self.online_mode:
            self._update_online_prices()
        else:
            self._update_offline_prices(active_news)

    def _update_offline_prices(self, active_news):
        # Determine current sector shock multipliers based on active news keywords
        shock_crypto = 1.0
        shock_stock = 1.0
        shock_forex = 1.0
        shock_all = 1.0

        if active_news:
            news_lower = active_news.lower()
            # Positive / negative rules
            positive_signals = ["pump", "accumulate", "approve", "rallies", "adopt", "surges", "green", "partnership"]
            negative_signals = ["hack", "down", "outage", "warns", "ban", "loss", "liquidate", "probe", "arrest"]

            direction = 1.0
            for ps in positive_signals:
                if ps in news_lower:
                    direction = 1.25
            for ns in negative_signals:
                if ns in news_lower:
                    direction = 0.75

            # Target sectors
            if any(k in news_lower for k in ["dog", "musk", "bitcoin", "ethereum", "solana", "crypto", "btc", "eth", "sol"]):
                shock_crypto = direction
            if any(k in news_lower for k in ["apple", "tesla", "tsla", "nvidia", "aapl", "nvda", "stock", "shares"]):
                shock_stock = direction
            if any(k in news_lower for k in ["fed", "powell", "inflation", "central bank", "interest rate"]):
                shock_all = direction
            if any(k in news_lower for k in ["forex", "eur", "usd", "jpy", "gbp"]):
                shock_forex = direction

        for ticker, meta in ASSET_CONFIG.items():
            base_vol = meta["volatility"]
            asset_type = meta["type"]

            # Select correct shock values
            sector_shock = 1.0
            if asset_type == "CRYPTO":
                sector_shock = shock_crypto
            elif asset_type == "STOCK":
                sector_shock = shock_stock
            elif asset_type == "FOREX":
                sector_shock = shock_forex

            final_shock = sector_shock * shock_all

            # Geometric random walk with mean-reverting trend momentum
            self.trends[ticker] += random.uniform(-0.01, 0.01)
            self.trends[ticker] = max(min(self.trends[ticker], 0.05), -0.05)
            
            drift = self.trends[ticker]
            # Random volatility perturbation
            change_pct = math.exp((drift - 0.5 * (base_vol ** 2)) + base_vol * random.gauss(0, 1))
            
            # Apply shock multiplier if news matches sector
            if final_shock != 1.0:
                change_pct *= (1.0 + (final_shock - 1.0) * base_vol)

            new_price = self.prices[ticker] * change_pct
            new_price = max(new_price, 0.0001)  # Safeguard asset value from hard zero

            self.prices[ticker] = round(new_price, 4)
            self.price_history[ticker].append(self.prices[ticker])
            if len(self.price_history[ticker]) > 30:
                self.price_history[ticker].pop(0)

    def _update_online_prices(self):
        # Fetch current asset coordinates using yfinance
        for ticker, meta in ASSET_CONFIG.items():
            yf_sym = meta["yf_ticker"]
            try:
                data = yf.Ticker(yf_sym).history(period="1d", interval="1m", timeout=5)
                if not data.empty:
                    current_val = float(data["Close"].iloc[-1])
                    self.prices[ticker] = round(current_val, 4)
                else:
                    # Fall back to simulation if no connection / rate limited
                    self._update_offline_prices(active_news=None)
            except Exception:
                # Fall back to simulation in case of exception
                self._update_offline_prices(active_news=None)
            
            self.price_history[ticker].append(self.prices[ticker])
            if len(self.price_history[ticker]) > 30:
                self.price_history[ticker].pop(0)

    def render_ascii_chart(self, ticker, height=6, width=40) -> str:
        history = self.price_history.get(ticker, [])
        if not history:
            return "No historical price coordinate set."
        if len(history) > width:
            history = history[-width:]
            
        min_p = min(history)
        max_p = max(history)
        delta = max_p - min_p if max_p != min_p else 1.0

        canvas = [[" " for _ in range(len(history))] for _ in range(height)]
        for col_idx, price in enumerate(history):
            norm_val = (price - min_p) / delta
            row_idx = int(norm_val * (height - 1))
            row_idx = max(0, min(row_idx, height - 1))
            # Invert height axis to place lowest values at bottom rows
            canvas[height - 1 - row_idx][col_idx] = "•"

        # Apply terminal block indicator on the last price point
        last_row = int(((history[-1] - min_p) / delta) * (height - 1))
        last_row = max(0, min(last_row, height - 1))
        canvas[height - 1 - last_row][-1] = "█"

        lines = []
        for row in range(height):
            line_str = "".join(canvas[row])
            if row == 0:
                lines.append(f"{line_str}  Max: {max_p:,.4f}")
            elif row == height - 1:
                lines.append(f"{line_str}  Min: {min_p:,.4f}")
            else:
                lines.append(line_str)
        return "\n".join(lines)