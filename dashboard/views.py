from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portfolio.models import Portfolio, Position
from trading.models import Trade

from stocks.models import Stock
from signals.models import Signal
from signals.services import generate_all_signals


@login_required
def home(request):
    return render(request, "dashboard/index.html")


@login_required
def dashboard(request):
    # generate_all_signals()
    # portfolio = Portfolio.objects.get(user=request.user)
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    positions = Position.objects.filter(portfolio=portfolio)
    trades = Trade.objects.filter(user=request.user).order_by("-created_at")
    signals = (Signal.objects.select_related("stock").order_by("-score"))

    context = {
    "portfolio": portfolio,
    "positions": positions,
    "backtest_runs": 12,  # Replace with actual count later
    "strong_buy": signals.filter(signal="STRONG BUY").count(),
    "buy": signals.filter(signal="BUY").count(),
    "hold": signals.filter(signal="HOLD").count(),
    "avoid": signals.filter(signal="AVOID").count(),
    "latest_signals": signals[:10],
    }
    return render(request,"dashboard/home.html",context)