# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from config import ASSET_CONFIG, LUXURY_SHOP

class UI:
    def __init__(self):
        self.console = Console()

    def render_splash_screen(self):
        self.console.clear()
        title_text = r"""
        ███╗   ██╗████████╗██████╗  █████╗ ██████╗ ███████╗
        ████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
        ██╔██╗ ██║   ██║   ██████╔╝███████║██║  ██║█████╗  
        ██║╚██╗██║   ██║   ██╔══██╗██╔══██║██║  ██║██╔══╝  
        ██║ ╚████║   ██║   ██║  ██║██║  ██║██████╔╝███████╗
        ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝
        """
        self.console.print(Align.center(Text(title_text, style="bright_cyan")))
        self.console.print(Align.center(Text("PRO-SPEC TERIMINAL FINANCIAL ENGINE v3.11", style="cyan underline")))
        self.console.print(Align.center(Text("\nDeveloped By Ben Timothy\n", style="bold green blink")))
        self.console.print(Align.center(Text("1. [N] Start New Simulation Game (Standard / Hardcore)", style="yellow")))
        self.console.print(Align.center(Text("2. [L] Load Game State Save Frame", style="yellow")))
        self.console.print(Align.center(Text("3. [Q] Quit Application System", style="red")))

    def render_dashboard(self, cash, net_worth, rank, ticks, mode_online, engine, desk, finance, active_news, last_action_log, selected_chart_asset):
        self.console.clear()
        
        # Build layout elements
        root = Layout()
        root.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=5)
        )

        # Header panel details
        is_hc_str = "[bold red]HARDCORE[/bold red]" if getattr(self, "hardcore_mode", False) else "[bright_green]STANDARD[/bright_green]"
        mode_str = "[green]ONLINE (LIVE)[/green]" if mode_online else "[yellow]OFFLINE (SIM)[/yellow]"
        header_table = Table.grid(expand=True)
        header_table.add_column(justify="left", ratio=1)
        header_table.add_column(justify="center", ratio=1)
        header_table.add_column(justify="right", ratio=1)
        header_table.add_row(
            f" [cyan]NTrade Simulator[/cyan] | Mode: {mode_str} | Mode Type: {is_hc_str}",
            f"[bold magenta]RANK: {rank}[/bold magenta] | Rep: [yellow]{finance.total_reputation} RP[/yellow]",
            f"Ticks Run: [bright_cyan]{ticks}[/bright_cyan] | [bold green]Developed By Ben Timothy[/bold green] "
        )
        root["header"].update(Panel(header_table, border_style="cyan"))

        # Main horizontal panels
        body_layout = Layout()
        body_layout.split_row(
            Layout(name="market_panel", ratio=2),
            Layout(name="chart_and_news", ratio=3),
            Layout(name="portfolio_panel", ratio=2)
        )
        root["body"].update(body_layout)

        # 1. Market Board Table
        market_table = Table(title="MARKET TICK DESK", style="cyan", expand=True, header_style="bold cyan")
        market_table.add_column("Ticker", style="bold yellow")
        market_table.add_column("Type", style="dim white")
        market_table.add_column("Price", justify="right", style="bright_green")
        market_table.add_column("Trend", justify="center")

        for ticker, meta in ASSET_CONFIG.items():
            price = engine.prices.get(ticker, 0.0)
            hist = engine.price_history.get(ticker, [])
            trend_icon = "[grey50]•[/grey50]"
            if len(hist) > 1:
                prev_p = hist[-2]
                if price > prev_p:
                    trend_icon = "[green]▲[/green]"
                elif price < prev_p:
                    trend_icon = "[red]▼[/red]"
            
            market_table.add_row(ticker, meta["type"], f"${price:,.4f}", trend_icon)

        body_layout["market_panel"].update(Panel(market_table, border_style="cyan"))

        # 2. Charting visual and news desk
        chart_layout = Layout()
        chart_layout.split_column(
            Layout(name="chart_area", ratio=3),
            Layout(name="news_area", ratio=1)
        )
        body_layout["chart_and_news"].update(chart_layout)

        chart_ascii = engine.render_ascii_chart(selected_chart_asset, height=7, width=42)
        chart_panel = Panel(
            f"[bold yellow]Ticker Chart: {selected_chart_asset}[/bold yellow]\n\n{chart_ascii}",
            border_style="yellow",
            title="GRAPHICAL ANALYSIS FEED"
        )
        chart_layout["chart_area"].update(chart_panel)

        display_news = active_news if active_news else "No fresh market events broadcasted currently."
        news_panel = Panel(f"[bold red]FEED[/bold red]: [cyan]{display_news}[/cyan]", border_style="red", title="MACRO ECONOMIC WIRE")
        chart_layout["news_area"].update(news_panel)

        # 3. Portfolio & Finance dashboard
        portfolio_text = Text()
        portfolio_text.append(f"Available Cash: ${cash:,.2f}\n", style="bold green")
        portfolio_text.append(f"Net Assets Valuation: ${net_worth:,.2f}\n", style="bold white")
        portfolio_text.append(f"Staked Savings: ${finance.staked_cash:,.2f}\n", style="cyan")
        portfolio_text.append(f"Outstanding Debt: ${finance.outstanding_loan:,.2f}\n\n", style="bold red")

        portfolio_text.append("=== ACTIVE POSITIONS ===\n", style="bold yellow")
        if not desk.positions:
            portfolio_text.append("No active open trading positions.\n", style="dim white")
        else:
            for p in desk.positions:
                cur_p = engine.prices.get(p.asset, p.entry_price)
                unrealized_pnl = p.calculate_pnl(cur_p)
                color = "green" if unrealized_pnl >= 0 else "red"
                portfolio_text.append(f"{p.direction} {p.asset} ({p.leverage}x) | Margin: ${p.margin:,.1f}\n PnL: ", style="bold white")
                portfolio_text.append(f"${unrealized_pnl:,.2f}\n", style=color)

        portfolio_text.append("\n=== PENDING LIMIT ORDERS ===\n", style="bold yellow")
        if not desk.limit_orders:
            portfolio_text.append("No active limit order parameters.\n", style="dim white")
        else:
            for lo in desk.limit_orders:
                portfolio_text.append(f"{lo.direction} {lo.asset} target @ ${lo.target_price:,.4f}\n", style="white")

        portfolio_panel = Panel(portfolio_text, border_style="cyan", title="PORTFOLIO & CAPITAL ACCOUNT")
        body_layout["portfolio_panel"].update(portfolio_panel)

        # Footer Panel
        footer_text = f"[bold green]System Operations Log:[/bold green] {last_action_log}\n"
        footer_text += "[bold yellow]Action Keys:[/bold yellow] [b]T[/b]: Tick Turn | [b]B[/b]: Buy/Long | [b]S[/b]: Sell/Short | [b]C[/b]: Close Position | [b]F[/b]: Yield Farm | [b]L[/b]: Bank Loans | [b]P[/b]: Shop Luxury | [b]A[/b]: Change Chart Ticker | [b]K[/b]: Toggle Online/Offline Mode | [b]Q[/b]: Exit System Save Frame"
        root["footer"].update(Panel(footer_text, border_style="magenta"))

        self.console.print(root)