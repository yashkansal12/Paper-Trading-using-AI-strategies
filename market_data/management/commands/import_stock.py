def import_stock_data(symbol):
    stock = Stock.objects.get(symbol=symbol)

    # Agar data already hai to dobara download mat karo
    if StockPrice.objects.filter(stock=stock).exists():
        return

    data = yf.download(
        symbol + ".NS",
        period="2y",
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        return

    for date, row in data.iterrows():
        StockPrice.objects.update_or_create(
            stock=stock,
            date=date.date(),
            defaults={
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            },
        )