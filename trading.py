# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

from config import TRANSACTION_FEE, MAINTENANCE_MARGIN

class Position:
    def __init__(self, asset, direction, entry_price, size, leverage, margin, tp=None, sl=None):
        self.asset = asset
        self.direction = direction  # 'LONG' or 'SHORT'
        self.entry_price = entry_price
        self.size = size            # Total position volume (margin * leverage / entry_price)
        self.leverage = leverage
        self.margin = margin        # Allocated cash margin
        self.tp = tp
        self.sl = sl

    def calculate_pnl(self, current_price) -> float:
        if self.direction == "LONG":
            return (current_price - self.entry_price) * self.size
        else:
            return (self.entry_price - current_price) * self.size

    def to_dict(self):
        return {
            "asset": self.asset,
            "direction": self.direction,
            "entry_price": self.entry_price,
            "size": self.size,
            "leverage": self.leverage,
            "margin": self.margin,
            "tp": self.tp,
            "sl": self.sl
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            asset=data["asset"],
            direction=data["direction"],
            entry_price=data["entry_price"],
            size=data["size"],
            leverage=data["leverage"],
            margin=data["margin"],
            tp=data.get("tp"),
            sl=data.get("sl")
        )

class LimitOrder:
    def __init__(self, asset, direction, target_price, size, leverage, margin, tp=None, sl=None):
        self.asset = asset
        self.direction = direction
        self.target_price = target_price
        self.size = size
        self.leverage = leverage
        self.margin = margin
        self.tp = tp
        self.sl = sl

    def to_dict(self):
        return {
            "asset": self.asset,
            "direction": self.direction,
            "target_price": self.target_price,
            "size": self.size,
            "leverage": self.leverage,
            "margin": self.margin,
            "tp": self.tp,
            "sl": self.sl
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            asset=data["asset"],
            direction=data["direction"],
            target_price=data["target_price"],
            size=data["size"],
            leverage=data["leverage"],
            margin=data["margin"],
            tp=data.get("tp"),
            sl=data.get("sl")
        )

class TradingDesk:
    def __init__(self):
        self.positions = []
        self.limit_orders = []

    def open_market_position(self, asset, direction, entry_price, margin, leverage, cash, tp=None, sl=None):
        notional_value = margin * leverage
        fee = notional_value * TRANSACTION_FEE
        total_cost = margin + fee

        if total_cost > cash:
            return False, "Insufficient cash resources to cover initial margin and fees."

        size = notional_value / entry_price
        pos = Position(asset, direction, entry_price, size, leverage, margin, tp, sl)
        self.positions.append(pos)
        return total_cost, f"Position successfully initialized. Fee: ${fee:,.2f}"

    def place_limit_order(self, asset, direction, target_price, margin, leverage, cash, tp=None, sl=None):
        notional_value = margin * leverage
        fee = notional_value * TRANSACTION_FEE
        total_cost = margin + fee

        if total_cost > cash:
            return False, "Insufficient cash reserve to authorize limit lock structure."

        size = notional_value / target_price
        order = LimitOrder(asset, direction, target_price, size, leverage, margin, tp, sl)
        self.limit_orders.append(order)
        # Lock margin from wallet during pending limit phase
        return total_cost, "Limit order successfully added to order book."

    def check_and_execute_limits(self, prices, cash):
        logs = []
        triggered = []
        for idx, order in enumerate(self.limit_orders):
            current_p = prices.get(order.asset)
            if not current_p:
                continue

            execute = False
            if order.direction == "LONG" and current_p <= order.target_price:
                execute = True
            elif order.direction == "SHORT" and current_p >= order.target_price:
                execute = True

            if execute:
                # Recalculate true size based on current execution price
                notional = order.margin * order.leverage
                true_size = notional / current_p
                pos = Position(order.asset, order.direction, current_p, true_size, order.leverage, order.margin, order.tp, order.sl)
                self.positions.append(pos)
                triggered.append(order)
                logs.append(f"[yellow]LIMIT FILLED[/yellow]: {order.direction} {order.asset} @ ${current_p:,.4f}")

        for order in triggered:
            self.limit_orders.remove(order)
        return logs

    def evaluate_risk_and_margins(self, prices):
        logs = []
        liquidated = []
        closed_tp_sl = []
        cash_refund = 0.0

        for pos in self.positions:
            current_p = prices.get(pos.asset)
            if not current_p:
                continue

            pnl = pos.calculate_pnl(current_p)
            equity = pos.margin + pnl

            # 1. Take Profit Evaluation
            if pos.tp is not None:
                if (pos.direction == "LONG" and current_p >= pos.tp) or (pos.direction == "SHORT" and current_p <= pos.tp):
                    closed_tp_sl.append(pos)
                    # Refund margin and pay real cash profit minus closing transaction fee
                    close_fee = (pos.size * current_p) * TRANSACTION_FEE
                    cash_refund += (pos.margin + pnl - close_fee)
                    logs.append(f"[green]TAKE PROFIT[/green]: Closed {pos.direction} {pos.asset} @ ${current_p:,.4f}. PnL: +${pnl:,.2f}")
                    continue

            # 2. Stop Loss Evaluation
            if pos.sl is not None:
                if (pos.direction == "LONG" and current_p <= pos.sl) or (pos.direction == "SHORT" and current_p >= pos.sl):
                    closed_tp_sl.append(pos)
                    close_fee = (pos.size * current_p) * TRANSACTION_FEE
                    cash_refund += max(0.0, pos.margin + pnl - close_fee)
                    logs.append(f"[red]STOP LOSS[/red]: Closed {pos.direction} {pos.asset} @ ${current_p:,.4f}. PnL: ${pnl:,.2f}")
                    continue

            # 3. Liquidation Evaluation
            # Check if current equity is below maintenance margin requirement (e.g. 15% of initial margin)
            if equity <= (pos.margin * MAINTENANCE_MARGIN):
                liquidated.append(pos)
                logs.append(f"[red]LIQUIDATION WARNING[/red]: {pos.direction} position on {pos.asset} margin wiped out. Liquidated @ ${current_p:,.4f}.")

        # Prune liquidated and TP/SL assets from books
        for pos in liquidated:
            self.positions.remove(pos)
        for pos in closed_tp_sl:
            self.positions.remove(pos)

        return cash_refund, logs