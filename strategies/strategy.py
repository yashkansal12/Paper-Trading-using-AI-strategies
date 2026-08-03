def generate_signal(stock, live_price, indicators):
    price = float(live_price or 0)
    ema20 = float(indicators.get("EMA20",0) or 0)
    ema50 = float(indicators.get("EMA50",0) or 0)
    ema200 = float(indicators.get("EMA200",0) or 0)
    rsi = float(indicators.get("RSI",0) or 0)
    volume = float(indicators.get("volume",0) or 0)
    avg_volume = float(indicators.get("avg_volume",0) or 0)


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

    # EMA Pullback
    if ema20 > ema50 and price >= ema20:
        score += 25
        reasons.append("EMA20 above EMA50")


    # RSI
    if 40 <= rsi <= 55:
        score += 20
        reasons.append("Healthy RSI")


    # Volume
    if volume > avg_volume:
        score += 15
        reasons.append("Volume above average")

    # Signal
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


    # Risk Management
    entry = price
    stop_loss = price * 0.98
    target = price * 1.10
    risk = abs(entry - stop_loss)
    reward = abs(target - entry)

    if risk == 0:
        rr = 0
    else:
        rr = round(reward / risk,2)

    # Risk Reward Score
    if rr >= 3:
        score += 10
        reasons.append("Good Risk Reward")

    return {
        "signal": signal,
        "score": score,
        "trend": trend,
        "confidence": score,
        "reason": " | ".join(reasons),
        "entry_price": round(entry,2),
        "target_price": round(target,2),
        "stop_loss": round(stop_loss,2),
        "risk_reward": rr,

    }