from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

from stocks.models import Stock
from .services import buy_stock, sell_stock
from stocks.service import get_live_stock_data

from django.contrib.auth.decorators import login_required
from .models import Trade
from django.shortcuts import render


def buy(request, pk):
    try:
        print("1. Buy view started")
        stock = Stock.objects.get(pk=pk)
        print("2. Stock:", stock.symbol)
        qty = int(request.POST["quantity"])
        print("3. Quantity:", qty)
        live = get_live_stock_data(stock.symbol)
        print("4. Live Price:", live["price"])

        success, message = buy_stock(
            request.user,
            stock,
            qty,
            live["price"],
        )

        print("5.", success, message)
        messages.success(request, message)
        print("6. Redirecting")
        return redirect("stock_detail", pk=pk)

    except Exception as e:
        print("ERROR:", e)
        return HttpResponse(f"<h2>{e}</h2>")


def sell(request, pk):

    stock = Stock.objects.get(pk=pk)
    qty = int(request.POST["quantity"])
    live = get_live_stock_data(stock.symbol)
    success, message = sell_stock(
        request.user,
        stock,
        qty,
        live["price"],
    )

    messages.success(request, message)
    return redirect("portfolio")





@login_required
def trade_history(request):
    trades = Trade.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request,"trading/history.html",{"trades": trades,},)