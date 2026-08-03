def calculate_metrics(result):

    initial_capital = result["initial_capital"]
    final_capital = result["final_capital"]

    trades = result["trades"]
    equity_curve = result["equity_curve"]

    # ------------------------
    # Return
    # ------------------------

    net_profit = final_capital - initial_capital

    return_percent = (
        (net_profit / initial_capital) * 100
        if initial_capital
        else 0
    )

    # ------------------------
    # Trades
    # ------------------------

    total_trades = len(trades)

    winning_trades = sum(
        1 for trade in trades
        if trade["profit"] > 0
    )

    losing_trades = sum(
        1 for trade in trades
        if trade["profit"] < 0
    )

    win_rate = (
        (winning_trades / total_trades) * 100
        if total_trades
        else 0
    )

    # ------------------------
    # Gross Profit/Loss
    # ------------------------

    gross_profit = sum(
        trade["profit"]
        for trade in trades
        if trade["profit"] > 0
    )

    gross_loss = abs(sum(
        trade["profit"]
        for trade in trades
        if trade["profit"] < 0
    ))

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 0
    )

    # ------------------------
    # Average Profit/Loss
    # ------------------------

    average_profit = (
        gross_profit / winning_trades
        if winning_trades
        else 0
    )

    average_loss = (
        gross_loss / losing_trades
        if losing_trades
        else 0
    )

    # ------------------------
    # Max Drawdown
    # ------------------------

    max_drawdown = 0

    if equity_curve:

        peak = equity_curve[0]["value"]

        for point in equity_curve:

            value = point["value"]

            if value > peak:
                peak = value

            drawdown = (
                (peak - value)
                / peak
            ) * 100

            if drawdown > max_drawdown:
                max_drawdown = drawdown

    # ------------------------
    # Results
    # ------------------------

    return {
        "initial_capital": round(initial_capital, 2),
        "final_capital": round(final_capital, 2),
        "net_profit": round(net_profit, 2),
        "return_percent": round(return_percent, 2),

        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(win_rate, 2),

        "gross_profit": round(gross_profit, 2),
        "gross_loss": round(gross_loss, 2),

        "average_profit": round(average_profit, 2),
        "average_loss": round(average_loss, 2),

        "profit_factor": round(profit_factor, 2),
        "max_drawdown": round(max_drawdown, 2),
    }