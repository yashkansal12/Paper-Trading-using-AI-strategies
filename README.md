# 📈 AI Stock Paper Trading Platform

A full-stack Django application that allows users to practice stock trading using virtual money while analyzing real market data with technical indicators and AI-based trading signals.

## 🚀 Features

- 🔐 User Authentication
- 📊 Live NSE Stock Prices
- 📈 Interactive Candlestick Charts (Plotly)
- 📉 Technical Indicators
  - EMA
  - SMA
  - RSI
- 🤖 AI Trading Signals
- 💼 Portfolio Management
- ⭐ Watchlist
- 🛒 Paper Trading
- 🎯 GTT Orders
- 🔄 Strategy Backtesting
- 📚 Historical Stock Data
- 🔍 Stock Search
- 📱 Responsive Bootstrap UI

## 🛠️ Tech Stack

- Python
- Django
- SQLite
- Pandas
- Plotly
- yfinance
- HTML
- CSS
- Bootstrap
- JavaScript

## Project Structure

```
accounts/
stocks/
dashboard/
signals/
strategies/
trading/
portfolio/
market_data/
backtesting/
gtt/
indicators/
templates/
static/
```

## Installation

```bash
git clone https://github.com/yashkansal12/Paper-Trading-using-AI-strategies.git
cd StockPaperTrading

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## Future Improvements

- PostgreSQL
- Redis Cache
- Celery Background Tasks
- Real-time WebSocket Updates
- Broker API Integration (Upstox/Angel One)
- News Sentiment Analysis
- Machine Learning-Based Predictions

## Author

Yash Kansal
