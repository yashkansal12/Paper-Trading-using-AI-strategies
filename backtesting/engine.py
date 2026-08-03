import pandas as pd

from stocks.models import Stock
from market_data.models import StockPrice

from .indicators import apply_indicators
from .strategy import generate_signals
from .executor import execute_trades
from .metrics import calculate_metrics



#CLAUDE CODE##


# class BacktestEngine:

#     def __init__(self, form_data):
#         self.form_data = form_data

#     def get_stocks(self):
#         symbols = self.form_data.get("symbols", "").strip()
#         if symbols:
#             symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
#             return Stock.objects.filter(symbol__in=symbol_list)
#         return Stock.objects.all()

#     def load_history(self, stock):
#         prices = StockPrice.objects.filter(
#             stock=stock,
#             date__range=(
#                 self.form_data["start_date"],
#                 self.form_data["end_date"],
#             ),
#         ).order_by("date")

#         if not prices.exists():
#             return None

#         return pd.DataFrame(
#             list(
#                 prices.values(
#                     "date",
#                     "open",
#                     "high",
#                     "low",
#                     "close",
#                     "volume",
#                 )
#             )
#         )

#     def run(self):
#         stocks = self.get_stocks()

#         processed = 0
#         total_candles = 0
#         selected_symbols = []
#         results = []

#         for stock in stocks:
#             df = self.load_history(stock)
#             if df is None or df.empty:
#                 continue

#             df = apply_indicators(df, self.form_data["strategy"])
#             df = generate_signals(df, self.form_data["strategy"])
#             trade_result = execute_trades(df, self.form_data["initial_capital"])
#             metrics = calculate_metrics(trade_result)
#             metrics["symbol"] = stock.symbol
#             results.append(metrics)

#             processed += 1
#             total_candles += len(df)
#             selected_symbols.append(stock.symbol)

#         if results:
#             total_initial = sum(r["initial_capital"] for r in results)
#             total_final = sum(r["final_capital"] for r in results)
#             total_profit = sum(r["net_profit"] for r in results)
#             total_trades = sum(r["total_trades"] for r in results)
#             winning_trades = sum(r["winning_trades"] for r in results)
#             losing_trades = sum(r["losing_trades"] for r in results)
#             return_percent = (total_profit / total_initial) * 100 if total_initial else 0
#             win_rate = (winning_trades / total_trades) * 100 if total_trades else 0

#             gross_profit = sum(r["gross_profit"] for r in results)
#             gross_loss = sum(r["gross_loss"] for r in results)
#             profit_factor = (gross_profit / gross_loss) if gross_loss else 0

#             average_profit = (gross_profit / winning_trades) if winning_trades else 0
#             average_loss = (gross_loss / losing_trades) if losing_trades else 0

#             max_drawdown = max((r["max_drawdown"] for r in results), default=0)
#         else:
#             total_initial = 0
#             total_final = 0
#             total_profit = 0
#             total_trades = 0
#             winning_trades = 0
#             losing_trades = 0
#             return_percent = 0
#             win_rate = 0
#             gross_profit = 0
#             gross_loss = 0
#             profit_factor = 0
#             average_profit = 0
#             average_loss = 0
#             max_drawdown = 0

#         return {
#             "strategy": self.form_data["strategy"],
#             "total_stocks": Stock.objects.count(),
#             "processed_stocks": processed,
#             "capital": self.form_data["initial_capital"],
#             "start_date": self.form_data["start_date"],
#             "end_date": self.form_data["end_date"],
#             "selected_symbols": selected_symbols,
#             "total_candles": total_candles,
#             "summary": {
#                 "initial_capital": round(total_initial, 2),
#                 "final_capital": round(total_final, 2),
#                 "net_profit": round(total_profit, 2),
#                 "return_percent": round(return_percent, 2),
#                 "total_trades": total_trades,
#                 "winning_trades": winning_trades,
#                 "losing_trades": losing_trades,
#                 "win_rate": round(win_rate, 2),
#                 "gross_profit": round(gross_profit, 2),
#                 "gross_loss": round(gross_loss, 2),
#                 "average_profit": round(average_profit, 2),
#                 "average_loss": round(average_loss, 2),
#                 "profit_factor": round(profit_factor, 2),
#                 "max_drawdown": round(max_drawdown, 2),
#             },
#             "results": results,
#         }











## CHATGPT CODE ##

class BacktestEngine:

    def __init__(self, form_data):
        self.form_data = form_data

    def get_stocks(self):
        symbols = self.form_data.get("symbols", "").strip()

        if symbols:
            symbol_list = [
                s.strip().upper()
                for s in symbols.split(",")
                if s.strip()
            ]
            return Stock.objects.filter(symbol__in=symbol_list)

        return Stock.objects.all()

    def load_history(self, stock):

        prices = (
            StockPrice.objects.filter(
                stock=stock,
                date__range=(
                    self.form_data["start_date"],
                    self.form_data["end_date"],
                ),
            )
            .order_by("date")
        )

        if not prices.exists():
            return None

        return pd.DataFrame(
            list(
                prices.values(
                    "date",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                )
            )
        )

    def run(self):

        stocks = self.get_stocks()

        processed = 0
        total_candles = 0

        selected_symbols = []
        results = []

        for stock in stocks:

            df = self.load_history(stock)

            if df is None or df.empty:
                continue

            df = apply_indicators(
                df,
                self.form_data["strategy"],
            )

            df = generate_signals(
                df,
                self.form_data["strategy"],
            )

            trade_result = execute_trades(
                df,
                self.form_data["initial_capital"],
            )

            metrics = calculate_metrics(trade_result)

            metrics["symbol"] = stock.symbol

            results.append(metrics)

            processed += 1
            total_candles += len(df)
            selected_symbols.append(stock.symbol)

        if results:

            total_initial = sum(
                r["initial_capital"]
                for r in results
            )

            total_final = sum(
                r["final_capital"]
                for r in results
            )

            total_profit = sum(
                r["net_profit"]
                for r in results
            )

            total_trades = sum(
                r["total_trades"]
                for r in results
            )

            winning_trades = sum(
                r["winning_trades"]
                for r in results
            )

            losing_trades = sum(
                r["losing_trades"]
                for r in results
            )

            return_percent = (
                (total_profit / total_initial) * 100
                if total_initial
                else 0
            )

            win_rate = (
                (winning_trades / total_trades) * 100
                if total_trades
                else 0
            )

            max_drawdown = max(
                r["max_drawdown"]
                for r in results
            )

            profit_factor = round(
                sum(
                    r["profit_factor"]
                    for r in results
                ) / len(results),
                2,
            )

            average_profit = round(
                sum(
                    r["average_profit"]
                    for r in results
                ) / len(results),
                2,
            )

            average_loss = round(
                sum(
                    r["average_loss"]
                    for r in results
                ) / len(results),
                2,
            )

        else:

            total_initial = 0
            total_final = 0
            total_profit = 0
            total_trades = 0
            winning_trades = 0
            losing_trades = 0
            return_percent = 0
            win_rate = 0
            max_drawdown = 0
            profit_factor = 0
            average_profit = 0
            average_loss = 0

        return {
            "strategy": self.form_data["strategy"],
            "total_stocks": Stock.objects.count(),
            "processed_stocks": processed,
            "capital": self.form_data["initial_capital"],
            "start_date": self.form_data["start_date"],
            "end_date": self.form_data["end_date"],
            "selected_symbols": selected_symbols,
            "total_candles": total_candles,
            "summary": {
                "initial_capital": round(
                    total_initial,
                    2,
                ),
                "final_capital": round(
                    total_final,
                    2,
                ),
                "net_profit": round(
                    total_profit,
                    2,
                ),
                "return_percent": round(
                    return_percent,
                    2,
                ),
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades,
                "win_rate": round(
                    win_rate,
                    2,
                ),
                "max_drawdown": round(
                    max_drawdown,
                    2,
                ),
                "profit_factor": profit_factor,
                "average_profit": average_profit,
                "average_loss": average_loss,
            },
            "results": results,
        }