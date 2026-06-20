# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

import sys
import os
import random
from config import INITIAL_CASH, NEWS_FEED, EXPENSE_INTERVAL_TICKS, EXPENSE_AMOUNT, LUXURY_SHOP, LEVERAGE_OPTIONS, ASSET_CONFIG
from database import init_db, save_game, load_game, get_slots, delete_save_file
from engine import MarketEngine
from trading import TradingDesk, Position, LimitOrder
from finance import FinancialManager
from ui import UI

class GameCoordinator:
    def __init__(self):
        self.ui = UI()
        self.engine = MarketEngine()
        self.desk = TradingDesk()
        self.finance = FinancialManager()

        self.cash = INITIAL_CASH
        self.net_worth = INITIAL_CASH
        self.rank = "Novice Trader"
        self.ticks_elapsed = 0
        self.active_news = ""
        self.last_log = "Simulation system initialized."
        self.selected_chart_asset = "BTC"
        
        self.slot_id = 1
        self.slot_name = "Default Slot"
        self.hardcore_mode = False
        self.is_dead = False

    def generate_save_dict(self):
        return {
            "cash": self.cash,
            "net_worth": self.net_worth,
            "rank": self.rank,
            "ticks_elapsed": self.ticks_elapsed,
            "active_news": self.active_news,
            "selected_chart_asset": self.selected_chart_asset,
            "online_mode": self.engine.online_mode,
            "prices": self.engine.prices,
            "price_history": self.engine.price_history,
            "staked_cash": self.finance.staked_cash,
            "outstanding_loan": self.finance.outstanding_loan,
            "owned_luxury": self.finance.owned_luxury,
            "total_reputation": self.finance.total_reputation,
            "positions": [pos.to_dict() for pos in self.desk.positions],
            "limit_orders": [order.to_dict() for order in self.desk.limit_orders]
        }

    def load_from_dict(self, state):
        self.cash = state.get("cash", INITIAL_CASH)
        self.net_worth = state.get("net_worth", INITIAL_CASH)
        self.rank = state.get("rank", "Novice Trader")
        self.ticks_elapsed = state.get("ticks_elapsed", 0)
        self.active_news = state.get("active_news", "")
        self.selected_chart_asset = state.get("selected_chart_asset", "BTC")
        self.engine.online_mode = state.get("online_mode", False)
        self.engine.prices = state.get("prices", self.engine.prices)
        self.engine.price_history = state.get("price_history", self.engine.price_history)
        
        self.finance.staked_cash = state.get("staked_cash", 0.0)
        self.finance.outstanding_loan = state.get("outstanding_loan", 0.0)
        self.finance.owned_luxury = state.get("owned_luxury", [])
        self.finance.total_reputation = state.get("total_reputation", 0)
        
        self.desk.positions = [Position.from_dict(p) for p in state.get("positions", [])]
        self.desk.limit_orders = [LimitOrder.from_dict(o) for o in state.get("limit_orders", [])]

    def trigger_auto_save(self):
        if not self.is_dead:
            save_game(
                self.slot_id,
                self.slot_name,
                self.generate_save_dict(),
                is_hardcore=int(self.hardcore_mode),
                is_dead=int(self.is_dead)
            )

    def advance_game_tick(self):
        self.ticks_elapsed += 1
        
        # 1. Update Market Prices
        self.engine.tick(self.active_news)

        # Reset news feed on each tick, random roll a new breaking event
        self.active_news = ""
        if random.random() < 0.20:
            self.active_news = random.choice(NEWS_FEED)

        # 2. Process Passive Finance Operations
        yield_earn, yield_msg = self.finance.process_staking_yield()
        interest_accrued, loan_msg = self.finance.process_loan_interest()

        # Update action logs from background triggers
        extra_logs = []
        if yield_msg:
            extra_logs.append(yield_msg)
        if loan_msg:
            extra_logs.append(loan_msg)

        # Proportional Monthly Life Expenses
        if self.ticks_elapsed % EXPENSE_INTERVAL_TICKS == 0:
            self.cash -= EXPENSE_AMOUNT
            extra_logs.append(f"[bold red]EXPENSE DEDUCTION[/bold red]: Charged ${EXPENSE_AMOUNT:,.2f} for living fees.")
            if self.cash < 0:
                # Force liquidation cascade to pay bills
                while self.cash < 0 and self.desk.positions:
                    pos = self.desk.positions.pop(0)
                    cur_p = self.engine.prices.get(pos.asset, pos.entry_price)
                    pnl = pos.calculate_pnl(cur_p)
                    self.cash += (pos.margin + pnl)
                    extra_logs.append(f"Auto-Liquidated {pos.asset} position due to negative cash flow.")

        # 3. Check Order Book Executions & Leverage Limits
        limits_log = self.desk.check_and_execute_limits(self.engine.prices, self.cash)
        extra_logs.extend(limits_log)

        refund_cash, risk_logs = self.desk.evaluate_risk_and_margins(self.engine.prices)
        self.cash += refund_cash
        extra_logs.extend(risk_logs)

        # 4. Loan Debt Collector Enforcement checks
        self.net_worth = self.finance.calculate_net_worth(self.cash, self.desk, self.engine.prices)
        collector_seized, collector_logs = self.finance.evaluate_debt_collector(self.net_worth, self.cash, self.desk)
        self.cash -= collector_seized
        extra_logs.extend(collector_logs)

        # Recalculate ranks & core balances
        self.net_worth = self.finance.calculate_net_worth(self.cash, self.desk, self.engine.prices)
        self.rank = self.finance.get_tier_rank(self.net_worth)

        # 5. Check Permadeath Constraints
        if self.net_worth <= 0.0:
            self.is_dead = True
            if self.hardcore_mode:
                self.ui.console.print("\n[bold red]FATAL: Net worth dropped below zero. Hardcore Permadeath Triggered! Save Slot Erased.[/bold red]\n")
                delete_save_file(self.slot_id)
                input("Press Enter to return to splash screen...")
                return False
            else:
                self.ui.console.print("\n[bold yellow]CRITICAL WARN: Net worth dropped below zero. Game over! Save slot remains persistent.[/bold yellow]\n")
                input("Press Enter to return to splash screen...")
                return False

        # Assemble logs for display
        if extra_logs:
            self.last_log = " | ".join(extra_logs)
        else:
            self.last_log = "Game tick advanced successfully."

        self.trigger_auto_save()
        return True

    def run(self):
        init_db()
        while True:
            self.ui.render_splash_screen()
            choice = input("\nSelect operational command: ").strip().lower()
            if choice == '1' or choice == 'n':
                self.new_game_flow()
            elif choice == '2' or choice == 'l':
                if self.load_game_flow():
                    self.game_loop()
            elif choice == '3' or choice == 'q':
                self.ui.console.print("System offline. Goodbye.")
                sys.exit(0)

    def new_game_flow(self):
        self.ui.console.clear()
        self.ui.console.print("[cyan]=== INITIALIZE NEW SAVE STREAM ===[/cyan]\n")
        slot = input("Select Game Save Slot (1-5): ").strip()
        try:
            self.slot_id = int(slot)
            if self.slot_id < 1 or self.slot_id > 5:
                raise ValueError
        except ValueError:
            self.ui.console.print("Invalid save slot default selection initialized on Slot 1.")
            self.slot_id = 1

        self.slot_name = input("Enter custom slot name: ").strip() or f"Trader Slot {self.slot_id}"
        hc_inp = input("Enable Hardcore Mode? (y/N): ").strip().lower()
        self.hardcore_mode = hc_inp == 'y'
        self.is_dead = False

        # Reset components
        self.engine = MarketEngine()
        self.desk = TradingDesk()
        self.finance = FinancialManager()
        self.cash = INITIAL_CASH
        self.net_worth = INITIAL_CASH
        self.ticks_elapsed = 0
        self.active_news = ""
        self.last_log = "New ledger workspace activated."
        
        self.trigger_auto_save()
        self.game_loop()

    def load_game_flow(self):
        self.ui.console.clear()
        self.ui.console.print("[cyan]=== CHOOSE PERSISTENT FRAME SAVE ===[/cyan]\n")
        slots = get_slots()
        if not slots:
            self.ui.console.print("No stored system frames detected. Press enter...")
            input()
            return False

        for sid, sname, is_hc, dead in slots:
            hc_tag = "[HARDCORE]" if is_hc else ""
            dead_tag = "[DEAD]" if dead else "ACTIVE"
            self.ui.console.print(f"Slot {sid}: [yellow]{sname}[/yellow] {hc_tag} - {dead_tag}")

        choice = input("\nEnter slot number to spin up: ").strip()
        try:
            target_id = int(choice)
            state, hc, dead = load_game(target_id)
            if state:
                if dead:
                    self.ui.console.print("[red]Critical: Attempted to load a dead state save. Permadeath lockout.[/red]")
                    input()
                    return False
                self.slot_id = target_id
                self.hardcore_mode = hc
                self.is_dead = dead
                self.load_from_dict(state)
                return True
            else:
                self.ui.console.print("Slot data is empty. Load canceled.")
                input()
                return False
        except ValueError:
            self.ui.console.print("Failed input formatting. Return to home dock.")
            input()
            return False

    def game_loop(self):
        # Set watermark mode dynamically within UI object reference
        setattr(self.ui, "hardcore_mode", self.hardcore_mode)
        
        while not self.is_dead:
            # Sync absolute net worth evaluation metrics
            self.net_worth = self.finance.calculate_net_worth(self.cash, self.desk, self.engine.prices)
            self.ui.render_dashboard(
                self.cash, self.net_worth, self.rank, self.ticks_elapsed,
                self.engine.online_mode, self.engine, self.desk, self.finance,
                self.active_news, self.last_log, self.selected_chart_asset
            )

            cmd = input("\nNT-Prompt> ").strip().lower()
            if not cmd:
                continue

            if cmd == 't':
                # Advance system timeframe tick
                if not self.advance_game_tick():
                    break
            elif cmd == 'b':
                self.ui_buy_flow()
            elif cmd == 's':
                self.ui_sell_flow()
            elif cmd == 'c':
                self.ui_close_flow()
            elif cmd == 'f':
                self.ui_staking_flow()
            elif cmd == 'l':
                self.ui_loan_flow()
            elif cmd == 'p':
                self.ui_shop_flow()
            elif cmd == 'a':
                self.ui_change_chart_flow()
            elif cmd == 'k':
                new_state = not self.engine.online_mode
                self.engine.set_online_mode(new_state)
                self.last_log = f"Market Engine mode toggled. Live values = {new_state}."
            elif cmd == 'q':
                self.trigger_auto_save()
                break

    def ui_buy_flow(self):
        self.ui.console.print("\n[yellow]Select Asset Ticker:[/yellow]")
        asset = input(", ".join(ASSET_CONFIG.keys()) + ": ").upper().strip()
        if asset not in ASSET_CONFIG:
            self.last_log = "Asset selection out of index boundary parameters."
            return

        order_type = input("Order Type (market/limit): ").strip().lower()
        direction = "LONG"  # Standard buy action defaults to long

        try:
            margin = float(input("Allocated Cash Margin size: $"))
            leverage = int(input(f"Leverage Multiple {LEVERAGE_OPTIONS}: "))
            if leverage not in LEVERAGE_OPTIONS:
                self.last_log = "Leverage scale coordinates locked out of compliance range."
                return

            tp = input("Take Profit target price (leave empty for none): ").strip()
            sl = input("Stop Loss target price (leave empty for none): ").strip()
            tp_val = float(tp) if tp else None
            sl_val = float(sl) if sl else None

            if order_type == "limit":
                target = float(input("Target execution limit price: $"))
                res, msg = self.desk.place_limit_order(asset, direction, target, margin, leverage, self.cash, tp_val, sl_val)
                if res is not False:
                    self.cash -= res
                    self.last_log = msg
                else:
                    self.last_log = msg
            else:
                entry = self.engine.prices[asset]
                res, msg = self.desk.open_market_position(asset, direction, entry, margin, leverage, self.cash, tp_val, sl_val)
                if res is not False:
                    self.cash -= res
                    self.last_log = msg
                else:
                    self.last_log = msg
        except ValueError:
            self.last_log = "Error during value conversion process."

        self.trigger_auto_save()

    def ui_sell_flow(self):
        self.ui.console.print("\n[red]Select Asset Ticker to SHORT Sell:[/red]")
        asset = input(", ".join(ASSET_CONFIG.keys()) + ": ").upper().strip()
        if asset not in ASSET_CONFIG:
            self.last_log = "Asset selection out of index parameters."
            return

        order_type = input("Order Type (market/limit): ").strip().lower()
        direction = "SHORT"

        try:
            margin = float(input("Allocated Cash Margin size: $"))
            leverage = int(input(f"Leverage Multiple {LEVERAGE_OPTIONS}: "))
            if leverage not in LEVERAGE_OPTIONS:
                self.last_log = "Leverage constraints violation."
                return

            tp = input("Take Profit target price (leave empty for none): ").strip()
            sl = input("Stop Loss target price (leave empty for none): ").strip()
            tp_val = float(tp) if tp else None
            sl_val = float(sl) if sl else None

            if order_type == "limit":
                target = float(input("Target execution limit short price: $"))
                res, msg = self.desk.place_limit_order(asset, direction, target, margin, leverage, self.cash, tp_val, sl_val)
                if res is not False:
                    self.cash -= res
                    self.last_log = msg
                else:
                    self.last_log = msg
            else:
                entry = self.engine.prices[asset]
                res, msg = self.desk.open_market_position(asset, direction, entry, margin, leverage, self.cash, tp_val, sl_val)
                if res is not False:
                    self.cash -= res
                    self.last_log = msg
                else:
                    self.last_log = msg
        except ValueError:
            self.last_log = "Formatting translation failed."

        self.trigger_auto_save()

    def ui_close_flow(self):
        if not self.desk.positions:
            self.last_log = "No open positions to dissolve."
            return

        self.ui.console.print("\n[yellow]Select Position ID to Close:[/yellow]")
        for idx, pos in enumerate(self.desk.positions):
            self.ui.console.print(f"{idx}: {pos.direction} {pos.asset} (Margin: ${pos.margin})")

        choice = input("Close Target Index: ").strip()
        try:
            index = int(choice)
            if index < 0 or index >= len(self.desk.positions):
                self.last_log = "Index outside margin parameters."
                return

            pos = self.desk.positions.pop(index)
            cur_p = self.engine.prices[pos.asset]
            pnl = pos.calculate_pnl(cur_p)
            closing_fee = (pos.size * cur_p) * 0.001
            net_proceeds = pos.margin + pnl - closing_fee

            self.cash += net_proceeds
            self.last_log = f"Closed {pos.asset} {pos.direction}. Realized PnL: ${pnl:,.2f}. Closing Fee: ${closing_fee:,.2f}"
        except ValueError:
            self.last_log = "Index processing failed."

        self.trigger_auto_save()

    def ui_staking_flow(self):
        self.ui.console.print(f"\n[cyan]Staking Vault Panel[/cyan] | Active Staked Cash: ${self.finance.staked_cash:,.2f}")
        action = input("Actions (stake / unstake): ").strip().lower()
        if action == "stake":
            try:
                amt = float(input("Stake Cash Value: $"))
                if amt <= 0 or amt > self.cash:
                    self.last_log = "Invalid transaction quantity value."
                else:
                    self.cash -= amt
                    self.finance.staked_cash += amt
                    self.last_log = f"Successfully locked ${amt:,.2f} inside staking pool."
            except ValueError:
                self.last_log = "Numerical verification parsing error."
        elif action == "unstake":
            try:
                amt = float(input("Unstake Cash Value: $"))
                if amt <= 0 or amt > self.finance.staked_cash:
                    self.last_log = "Requested yield withdrawal out of balance metrics."
                else:
                    self.finance.staked_cash -= amt
                    self.cash += amt
                    self.last_log = f"Unlocked ${amt:,.2f} from yield generator."
            except ValueError:
                self.last_log = "Numeric evaluation parse error."

        self.trigger_auto_save()

    def ui_loan_flow(self):
        self.ui.console.print(f"\n[red]Bank Loan Administration Desk[/red] | Debt: ${self.finance.outstanding_loan:,.2f}")
        action = input("Actions (borrow / repay): ").strip().lower()
        if action == "borrow":
            # Cap maximum borrow bounds at 50% of evaluated net worth
            max_borrow = self.net_worth * 0.5
            self.ui.console.print(f"Maximum calculated debt authorization limit: ${max_borrow:,.2f}")
            try:
                amt = float(input("Enter loan amount request: $"))
                if amt <= 0 or (self.finance.outstanding_loan + amt) > max_borrow:
                    self.last_log = "Request rejected. Credit limit violation constraints."
                else:
                    self.finance.outstanding_loan += amt
                    self.cash += amt
                    self.last_log = f"Bank authorized loan line. Disbursed ${amt:,.2f} cash."
            except ValueError:
                self.last_log = "Parsing loan conversion failure."
        elif action == "repay":
            try:
                amt = float(input("Enter cash value to pay back: $"))
                if amt <= 0 or amt > self.cash or amt > self.finance.outstanding_loan:
                    self.last_log = "Repayment execution parameters out of range bounds."
                else:
                    self.cash -= amt
                    self.finance.outstanding_loan -= amt
                    self.last_log = f"Processed repayment: -${amt:,.2f} debt principal value."
            except ValueError:
                self.last_log = "Numerical processing conversion exception."

        self.trigger_auto_save()

    def ui_shop_flow(self):
        self.ui.console.print("\n[yellow]=== STATUS LUXURY CATALOGUE ===[/yellow]\n")
        for key, item in LUXURY_SHOP.items():
            owned_status = "[OWNED]" if key in self.finance.owned_luxury else "[AVAILABLE]"
            self.ui.console.print(f"ID: {key} | {item['name']} | Cost: ${item['cost']:,.2f} | Status Reputation: +{item['rep']} RP | {owned_status}")

        choice = input("\nEnter Object ID to purchase: ").strip().lower()
        if choice in LUXURY_SHOP:
            res, msg = self.finance.buy_luxury_item(choice, self.cash)
            if res is not False:
                self.cash -= res
                self.last_log = msg
            else:
                self.last_log = msg
        else:
            self.last_log = "Invalid store catalogue reference parameter."

        self.trigger_auto_save()

    def ui_change_chart_flow(self):
        self.ui.console.print("\n[cyan]Enter target chart asset ticker symbol:[/cyan]")
        target = input(", ".join(ASSET_CONFIG.keys()) + ": ").strip().upper()
        if target in ASSET_CONFIG:
            self.selected_chart_asset = target
            self.last_log = f"Graph engine switched viewport focal target to: {target}."
        else:
            self.last_log = "Invalid asset selection target parameters."

if __name__ == "__main__":
    coordinator = GameCoordinator()
    coordinator.run()