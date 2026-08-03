import numpy as np


def generate_signals(df, strategy):

    df["signal"] = "HOLD"

    strategy = strategy.lower()

    if strategy == "ema":

        df.loc[
            df["EMA20"] > df["EMA50"],
            "signal"
        ] = "BUY"

        df.loc[
            df["EMA20"] < df["EMA50"],
            "signal"
        ] = "SELL"

    elif strategy == "sma":

        df.loc[
            df["SMA20"] > df["SMA50"],
            "signal"
        ] = "BUY"

        df.loc[
            df["SMA20"] < df["SMA50"],
            "signal"
        ] = "SELL"

    elif strategy == "rsi":

        df.loc[df["RSI"] < 30, "signal"] = "BUY"
        df.loc[df["RSI"] > 70, "signal"] = "SELL"

    elif strategy == "macd":

        df.loc[
            df["MACD"] > df["MACD_SIGNAL"],
            "signal"
        ] = "BUY"

        df.loc[
            df["MACD"] < df["MACD_SIGNAL"],
            "signal"
        ] = "SELL"

    elif strategy == "volume":

        df.loc[
            df["volume"] > df["VOLUME_SMA20"],
            "signal"
        ] = "BUY"

        df.loc[
            df["volume"] < df["VOLUME_SMA20"],
            "signal"
        ] = "SELL"

    elif strategy == "vwap":

        df.loc[
            df["close"] > df["VWAP"],
            "signal"
        ] = "BUY"

        df.loc[
            df["close"] < df["VWAP"],
            "signal"
        ] = "SELL"

    return df