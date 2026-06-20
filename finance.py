# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

from config import STAKING_YIELD_RATE, LOAN_INTEREST_RATE, DEBT_REPOSSESSION_RATIO, PROGRESSION_RANKS, LUXURY_SHOP

class FinancialManager:
    def __init__(self):
        self.staked_cash = 0.0
        self.outstanding_loan = 0.0
        self.owned_luxury = []
        self.total_reputation = 0

    def calculate_net_worth(self, cash, trading_desk, current_prices) -> float:
        net_worth = cash + self.staked_cash - self.outstanding_loan
        # Add unrealized equity across open positions
        for pos in trading_desk.positions:
            p_val = current_prices.get(pos.asset, pos.entry_price)
            net_worth += (pos.margin + pos.calculate_pnl(p_val))
        # Add values from pending limit order margin blocks
        for order in trading_desk.limit_orders:
            net_worth += order.margin
        return round(net_worth, 2)

    def process_staking_yield(self) -> tuple[float, str]:
        if self.staked_cash <= 0:
            return 0.0, ""
        yield_earned = self.staked_cash * STAKING_YIELD_RATE
        self.staked_cash += yield_earned
        return yield_earned, f"Accrued yield on staked vault: +${yield_earned:,.2f}"

    def process_loan_interest(self) -> tuple[float, str]:
        if self.outstanding_loan <= 0:
            return 0.0, ""
        interest = self.outstanding_loan * LOAN_INTEREST_RATE
        self.outstanding_loan += interest
        return interest, f"Accrued outstanding bank loan interest: +${interest:,.2f}"

    def evaluate_debt_collector(self, net_worth, cash, trading_desk) -> tuple[float, list[str]]:
        logs = []
        payment_extracted = 0.0
        # Check if outstanding loan is in breach (greater than 150% of total net worth)
        if self.outstanding_loan > 0 and self.outstanding_loan > (net_worth * DEBT_REPOSSESSION_RATIO):
            logs.append("[bold red]DEBT COLLECTOR BREACH WARNING[/bold red]: Loan exceeds collateral metrics.")
            # Force extract from cash
            if cash > 0:
                extract = min(cash, self.outstanding_loan)
                cash -= extract
                self.outstanding_loan -= extract
                payment_extracted += extract
                logs.append(f"Debt Collector seized ${extract:,.2f} from available cash.")

            # If debt remains, liquidate positions or luxury items
            if self.outstanding_loan > 0 and trading_desk.positions:
                pos = trading_desk.positions.pop(0)
                self.outstanding_loan = max(0.0, self.outstanding_loan - pos.margin)
                logs.append(f"Debt Collector forcefully liquidated your {pos.asset} position.")

            if self.outstanding_loan > 0 and self.owned_luxury:
                item_key = self.owned_luxury.pop(0)
                item_data = LUXURY_SHOP.get(item_key)
                if item_data:
                    resale_val = item_data["cost"] * 0.5
                    self.outstanding_loan = max(0.0, self.outstanding_loan - resale_val)
                    self.total_reputation = max(0, self.total_reputation - item_data["rep"])
                    logs.append(f"Debt Collector seized your luxury {item_data['name']} (Sold at 50% value).")

        return payment_extracted, logs

    def get_tier_rank(self, net_worth) -> str:
        current_rank = PROGRESSION_RANKS[0][1]
        for threshold, rank in PROGRESSION_RANKS:
            if net_worth >= threshold:
                current_rank = rank
        return current_rank

    def buy_luxury_item(self, item_id, cash) -> tuple[bool, str]:
        item = LUXURY_SHOP.get(item_id)
        if not item:
            return False, "Requested luxury object variant does not exist."
        if item_id in self.owned_luxury:
            return False, "You already possess this unique status asset."
        if cash < item["cost"]:
            return False, "Inadequate liquidation cash reserves to perform luxury acquisition."

        self.owned_luxury.append(item_id)
        self.total_reputation += item["rep"]
        return item["cost"], f"Acquired luxury item: {item['name']}. Status Reputation increased!"