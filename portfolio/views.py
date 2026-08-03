from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from stocks.models import Stock
from .models import Watchlist
from django.contrib.auth.decorators import login_required
from .models import Portfolio
from decimal import Decimal
from stocks.service import get_live_stock_data
from market_data.models import StockPrice


@login_required
def add_watchlist(request,id):
    stock = Stock.objects.get(id=id)
    Watchlist.objects.get_or_create(user=request.user,stock=stock)
    return redirect("stock_detail",pk=id)

@login_required
def watchlist(request):
    stocks = Watchlist.objects.filter(user=request.user)
    return render(request,"portfolio/watchlist.html",{"stocks":stocks})





@login_required
def portfolio_dashboard(request):
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    positions = portfolio.positions.all()

    total_value = Decimal("0")
    total_pnl = Decimal("0")

    for position in positions:

        live = get_live_stock_data(position.stock.symbol)

        if live:
            current_price = Decimal(str(live["price"]))
        else:
            latest = (
                StockPrice.objects
                .filter(stock=position.stock)
                .order_by("-date")
                .first()
            )

            current_price = (
                Decimal(str(latest.close))
                if latest
                else position.average_price
            )

        position.current_price = current_price
        position.market_value = current_price * position.quantity
        position.unrealized_pnl = (
            current_price - position.average_price
        ) * position.quantity

        total_value += position.market_value
        total_pnl += position.unrealized_pnl

    portfolio.portfolio_value = total_value
    portfolio.total_pnl = total_pnl

    return render(request,"portfolio/dashboard.html",{"portfolio": portfolio,"positions": positions,},)