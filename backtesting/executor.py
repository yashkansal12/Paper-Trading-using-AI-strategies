def execute_trades(df, initial_capital):

    cash = float(initial_capital)
    shares = 0

    trades = []
    equity_curve = []

    buy_price = None
    buy_date = None

    for _, row in df.iterrows():

        price = float(row["close"])
        signal = row["signal"]

        # BUY
        if signal == "BUY" and shares == 0:

            shares = int(cash // price)

            if shares > 0:

                cash -= shares * price

                buy_price = price
                buy_date = row["date"]

        # SELL
        elif signal == "SELL" and shares > 0:

            sell_price = price
            sell_date = row["date"]

            cash += shares * sell_price

            profit = (sell_price - buy_price) * shares

            profit_percent = (
                (sell_price - buy_price)
                / buy_price
            ) * 100

            trades.append({
                "buy_date": buy_date,
                "sell_date": sell_date,
                "buy_price": round(buy_price, 2),
                "sell_price": round(sell_price, 2),
                "shares": shares,
                "profit": round(profit, 2),
                "profit_percent": round(profit_percent, 2),
            })

            shares = 0
            buy_price = None
            buy_date = None

        portfolio_value = cash + (shares * price)

        equity_curve.append({
            "date": row["date"],
            "value": round(portfolio_value, 2),
        })

    # Close any open position using last close

    if len(df):

        last_price = float(df.iloc[-1]["close"])

        final_capital = cash + (shares * last_price)

    else:

        final_capital = cash

    return {
        "initial_capital": float(initial_capital),
        "final_capital": round(final_capital, 2),
        "cash": round(cash, 2),
        "open_shares": shares,
        "trades": trades,
        "equity_curve": equity_curve,
    }