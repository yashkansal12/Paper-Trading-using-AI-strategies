import yfinance as yf


def get_live_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol + ".NS")
        info = ticker.fast_info
        price = info.get("lastPrice")
        previous_close = info.get("previousClose")
        if price is None:
            return None

        if previous_close is None:
            previous_close = price

        change = price - previous_close
        change_percent = (
            change / previous_close * 100
            if previous_close != 0
            else 0
        ) 

        return {
             "price": round(price, 2),
             "open": round(info.get("open") or 0, 2),
             "high": round(info.get("dayHigh") or 0, 2),
             "low": round(info.get("dayLow") or 0, 2),
             "volume": info.get("lastVolume") or 0,
             "change": round(change, 2),
             "change_percent": round(change_percent, 2),
             }

    except Exception as e:
        print("Live Data Error:",symbol,e)
        return None