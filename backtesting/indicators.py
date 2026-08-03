import pandas as pd


def apply_indicators(df, strategy):

    strategy = strategy.lower()

    # EMA
    if strategy == "ema":
        df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
        df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

    # SMA
    elif strategy == "sma":
        df["SMA20"] = df["close"].rolling(window=20).mean()
        df["SMA50"] = df["close"].rolling(window=50).mean()

    # RSI
    elif strategy == "rsi":

        delta = df["close"].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    elif strategy == "macd":

        ema12 = df["close"].ewm(span=12, adjust=False).mean()
        ema26 = df["close"].ewm(span=26, adjust=False).mean()

        df["MACD"] = ema12 - ema26
        df["MACD_SIGNAL"] = (
            df["MACD"]
            .ewm(span=9, adjust=False)
            .mean()
        )
        df["MACD_HIST"] = (
            df["MACD"] - df["MACD_SIGNAL"]
        )

    # Volume
    elif strategy == "volume":

        df["VOLUME_SMA20"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )

    # VWAP
    elif strategy == "vwap":

        typical_price = (
            df["high"] +
            df["low"] +
            df["close"]
        ) / 3

        df["VWAP"] = (
            (typical_price * df["volume"]).cumsum()
            / df["volume"].cumsum()
        )

    return df