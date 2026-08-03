import yfinance as yf
from stocks.models import Stock
from market_data.models import StockPrice


def import_stock_data(symbol):
    stock = Stock.objects.get(symbol=symbol)

    # Agar data pehle se hai to dobara download mat karo
    if StockPrice.objects.filter(stock=stock).exists():
        return

    ticker = yf.Ticker(symbol + ".NS")
    df = ticker.history(period="2y")

    if df.empty:
        return

    for index, row in df.iterrows():
        StockPrice.objects.update_or_create(
            stock=stock,
            date=index.date(),
            defaults={
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            },
        )

    return True



def get_market_indices():
    symbols = {
        "nifty": "^NSEI",
        "sensex": "^BSESN",
        "banknifty": "^NSEBANK",
        "indiavix": "^INDIAVIX",
    }
    data = {}
    for name, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            current = info["lastPrice"]
            previous = info["previousClose"]
            change = current - previous
            percent = (change / previous) * 100
            data[name] = {
                "price": round(current, 2),
                "change": round(change, 2),
                "percent": round(percent, 2),
            }
            
        except Exception:
            data[name] = {"price": "--","change": "--","percent": "--",}
    return data