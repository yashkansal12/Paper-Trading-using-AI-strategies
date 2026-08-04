from stocks.models import Stock
from stocks.service import get_live_stock_data
from market_data.models import StockPrice

from .models import Signal
from .strategy import generate_signal


def generate_all_signals():
    """
    Generate signals for all active stocks.
    """
    
    
    
    
    

    # stocks = Stock.objects.filter(is_active=True)[:500]
    stocks = Stock.objects.filter(is_active=True)[500:1500]
    
    
    

    


    for stock in stocks:

        try:
            # -----------------------------
            # Live Price
            # -----------------------------
            live = get_live_stock_data(stock.symbol)

            if not live:
                continue

            # -----------------------------
            # Historical Data
            # -----------------------------
            prices = (
                StockPrice.objects
                .filter(stock=stock)
                .order_by("date")
            )

            # if prices.count() < 200:
            #     continue

            if prices.count() < 20:
                continue

            closes = [float(p.close) for p in prices]
            volumes = [float(p.volume) for p in prices]

            # -----------------------------
            # EMA (Simple Approximation)
            # -----------------------------
            ema20 = sum(closes[-20:]) / 20
            ema50 = sum(closes[-50:]) / 50
            ema200 = sum(closes[-200:]) / 200

            # -----------------------------
            # RSI (14)
            # -----------------------------
            gains = []
            losses = []

            for i in range(1, 15):
                change = closes[-15 + i] - closes[-16 + i]

                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))

            avg_gain = sum(gains) / 14
            avg_loss = sum(losses) / 14

            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))

            # -----------------------------
            # Volume
            # -----------------------------
            current_volume = volumes[-1]
            average_volume = sum(volumes[-20:]) / 20

            indicators = {
                "EMA20": ema20,
                "EMA50": ema50,
                "EMA200": ema200,
                "RSI": rsi,
                "volume": current_volume,
                "avg_volume": average_volume,
            }

            # -----------------------------
            # Strategy
            # -----------------------------
            result = generate_signal(
                stock=stock,
                live_price=live["price"],
                indicators=indicators,
            )

            print("=" * 60)
            print(f"Stock : {stock.symbol}")
            print(f"Price : {live['price']}")
            print(f"EMA20 : {ema20:.2f}")
            print(f"EMA50 : {ema50:.2f}")
            print(f"EMA200: {ema200:.2f}")
            print(f"RSI : {rsi:.2f}")
            print(f"Volume : {current_volume}")
            print(f"Avg Volume : {average_volume}")
            print(result)

            
            Signal.objects.update_or_create(
                stock=stock,
                defaults={
                    "signal": result["signal"],
                    "score": result["score"],
                    "trend": result["trend"],
                    "confidence": result["confidence"],
                    "reason": result["reason"],
                    "entry_price": result["entry_price"],
                    "target_price": result["target_price"],
                    "stop_loss": result["stop_loss"],
                    "risk_reward": result["risk_reward"],
                },
            )

        except Exception as e:
            print(f"{stock.symbol}: {e}")









# from stocks.models import Stock
# from stocks.service import get_live_stock_data
# from market_data.models import StockPrice

# from .models import Signal
# from .strategy import generate_signal


# def generate_all_signals():
#     """
#     Generate signals for all active stocks.
#     """

#     stocks = Stock.objects.filter(is_active=True)[:50]

#     for stock in stocks:

#         try:
#             # -----------------------------
#             # Live Price
#             # -----------------------------
#             live = get_live_stock_data(stock.symbol)

#             if not live:
#                 continue

#             # -----------------------------
#             # Historical Data
#             # -----------------------------
#             prices = (
#                 StockPrice.objects
#                 .filter(stock=stock)
#                 .order_by("date")
#             )

#             # if prices.count() < 200:
#             #     continue

#             if prices.count() < 20:
#                 continue

#             closes = [float(p.close) for p in prices]
#             volumes = [float(p.volume) for p in prices]

#             # -----------------------------
#             # EMA (Simple Approximation)
#             # -----------------------------
#             ema20 = sum(closes[-20:]) / 20
#             ema50 = sum(closes[-50:]) / 50
#             ema200 = sum(closes[-200:]) / 200

#             # -----------------------------
#             # RSI (14)
#             # -----------------------------
#             gains = []
#             losses = []

#             for i in range(1, 15):
#                 change = closes[-15 + i] - closes[-16 + i]

#                 if change > 0:
#                     gains.append(change)
#                     losses.append(0)
#                 else:
#                     gains.append(0)
#                     losses.append(abs(change))

#             avg_gain = sum(gains) / 14
#             avg_loss = sum(losses) / 14

#             if avg_loss == 0:
#                 rsi = 100
#             else:
#                 rs = avg_gain / avg_loss
#                 rsi = 100 - (100 / (1 + rs))

#             # -----------------------------
#             # Volume
#             # -----------------------------
#             current_volume = volumes[-1]
#             average_volume = sum(volumes[-20:]) / 20

#             indicators = {
#                 "EMA20": ema20,
#                 "EMA50": ema50,
#                 "EMA200": ema200,
#                 "RSI": rsi,
#                 "volume": current_volume,
#                 "avg_volume": average_volume,
#             }

#             # -----------------------------
#             # Strategy
#             # -----------------------------
#             result = generate_signal(
#                 stock=stock,
#                 live_price=live["price"],
#                 indicators=indicators,
#             )

#             print("=" * 60)
#             print(f"Stock : {stock.symbol}")
#             print(f"Price : {live['price']}")
#             print(f"EMA20 : {ema20:.2f}")
#             print(f"EMA50 : {ema50:.2f}")
#             print(f"EMA200: {ema200:.2f}")
#             print(f"RSI : {rsi:.2f}")
#             print(f"Volume : {current_volume}")
#             print(f"Avg Volume : {average_volume}")
#             print(result)

            
#             Signal.objects.update_or_create(
#                 stock=stock,
#                 defaults={
#                     "signal": result["signal"],
#                     "score": result["score"],
#                     "trend": result["trend"],
#                     "confidence": result["confidence"],
#                     "reason": result["reason"],
#                     "entry_price": result["entry_price"],
#                     "target_price": result["target_price"],
#                     "stop_loss": result["stop_loss"],
#                     "risk_reward": result["risk_reward"],
#                 },
#             )

#         except Exception as e:
#             print(f"{stock.symbol}: {e}")