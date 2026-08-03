def generate_signal(stock, live_price, indicators):

    price = float(live_price)

    ema20 = float(indicators["EMA20"])
    ema50 = float(indicators["EMA50"])
    ema200 = float(indicators["EMA200"])
    rsi = float(indicators["RSI"])
    volume = float(indicators["volume"])
    avg_volume = float(indicators["avg_volume"])

    score = 0
    reasons = []

    # Trend
    if price > ema200:
        score += 30
        trend = "Bullish"
        reasons.append("Price above EMA200")
    else:
        trend = "Bearish"
        reasons.append("Price below EMA200")

    # EMA
    if ema20 > ema50 and price >= ema20:
        score += 25
        reasons.append("EMA20 above EMA50")

    # RSI
    if 40 <= rsi <= 55:
        score += 20
        reasons.append("Healthy RSI")
    elif 30 <= rsi < 40:
        score += 10
        reasons.append("RSI Recovering")

    # Volume
    if volume > avg_volume:
        score += 15
        reasons.append("Volume Above Average")

    # Final Signal
    if score >= 80:
        signal = "STRONG BUY"
    elif score >= 65:
        signal = "BUY"
    elif score >= 50:
        signal = "WATCH"
    elif score >= 30:
        signal = "HOLD"
    else:
        signal = "AVOID"

    # Risk Reward
    entry = price

    if signal == "STRONG BUY":
        stop_loss = min(ema20, price * 0.98)
        target = price + (price - stop_loss) * 3
    elif signal == "BUY":
        stop_loss = min(ema50, price * 0.98)
        target = price + (price - stop_loss) * 2
    elif signal == "WATCH":
        stop_loss = min(ema50, price * 0.99)
        target = price + (price - stop_loss) * 1.5
    else:
        stop_loss = price
        target = price

    risk = abs(price - stop_loss)
    reward = abs(target - price)

    if risk > 0:
        rr = round(reward / risk, 2)
    else:
        rr = 0

    if rr >= 3:
        score += 10
        reasons.append("Good Risk Reward")

    return {
        "stock": stock,
        "signal": signal,
        "score": score,
        "trend": trend,
        "confidence": score,
        "reason": "\n".join(reasons),
        "entry_price": round(entry, 2),
        "target_price": round(target, 2),
        "stop_loss": round(stop_loss, 2),
        "risk_reward": rr,
    }