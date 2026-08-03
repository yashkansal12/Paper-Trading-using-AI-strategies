import pandas as pd
from .models import UserIndicator



def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


def calculate_sma(df, period):
    return df["close"].rolling(period).mean()



# def get_user_indicators(user, df):

#     indicators = UserIndicator.objects.filter(
#         user=user,
#         is_enabled=True
#     )

#     results = {}

#     for indicator in indicators:

#         if indicator.indicator == "RSI":
#             results["RSI"] = calculate_rsi(
#                 df,
#                 indicator.period
#             ).iloc[-1]

#         elif indicator.indicator == "EMA":
#             results[f"EMA {indicator.period}"] = calculate_ema(
#                 df,
#                 indicator.period
#             ).iloc[-1]

#         elif indicator.indicator == "SMA":
#             results[f"SMA {indicator.period}"] = calculate_sma(
#                 df,
#                 indicator.period
#             ).iloc[-1]

#     return results



def apply_user_indicators(user, df):

    indicators = UserIndicator.objects.filter(
        user=user,
        enabled=True
    )

    for item in indicators:

        if item.indicator == "EMA":
            column = f"EMA{item.period}"
            df[column] = calculate_ema(df, item.period)

        elif item.indicator == "SMA":
            column = f"SMA{item.period}"
            df[column] = calculate_sma(df, item.period)

        elif item.indicator == "RSI":
            column = f"RSI{item.period}"
            df[column] = calculate_rsi(df, item.period)

    return df