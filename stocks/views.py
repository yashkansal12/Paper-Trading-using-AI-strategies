from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from .models import Stock
from django.db.models import Q
from .models import Stock, StockMaster
from .service import get_live_stock_data

from market_data.models import StockPrice
from market_data.services import import_stock_data

# from indicators.services import calculate_rsi
from indicators.services import apply_user_indicators
from indicators.models import UserIndicator
from indicators.forms import UserIndicatorForm
from strategies.strategy import generate_signal

import pandas as pd
import yfinance as yf

from django.http import HttpResponse

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots



@login_required
def stock_list(request):

    stocks=Stock.objects.all()[:200]    #for number of stocks in stock list 
    stock_data=[]

    for stock in stocks:

        try:
            live=get_live_stock_data(stock.symbol)

            if live is None:
                live={
                    "price":0,
                    "open":0,
                    "high":0,
                    "low":0,
                    "volume":0,
                    "change":0,
                    "change_percent":0,
                }

        except Exception as e:
            print(stock.symbol,e)

            live={
                "price":0,
                "open":0,
                "high":0,
                "low":0,
                "volume":0,
                "change":0,
                "change_percent":0,
            }


        stock_data.append({
            "stock":stock,
            "live":live
        })


    return render(request,"stocks/stock_list.html",{"stock_data":stock_data})



# @login_required
# def stock_list(request):
#     stocks = Stock.objects.all()
#     return render(request,"stocks/stock_list.html",{"stocks": stocks,},)




@login_required
def search_stock(request):
    query = request.GET.get("q", "").strip().upper()
    stocks = StockMaster.objects.none()
    if query:
        stocks = StockMaster.objects.filter(
            Q(symbol__icontains=query) |
            Q(company_name__icontains=query)
        ).order_by("symbol")[:30]

    return render(request,"stocks/search.html",{"stocks": stocks,"query": query,},)


@login_required
def stock_detail(request,pk):
    stock=get_object_or_404(
        Stock,
        pk=pk
    )

    live=get_live_stock_data(stock.symbol)

    if live is None:
        live={
            "price":0,
            "open":0,
            "high":0,
            "low":0,
            "volume":0,
            "change":0,
            "change_percent":0,
        }

    prices=StockPrice.objects.filter(
        stock=stock
    ).order_by("date")

    df=pd.DataFrame({

        "date":[p.date for p in prices],
        "open":[float(p.open) for p in prices],
        "high":[float(p.high) for p in prices],
        "low":[float(p.low) for p in prices],
        "close":[float(p.close) for p in prices],
        "volume":[int(p.volume) for p in prices],

    })


    if df.empty:

        return render(
            request,
            "stocks/stock_detail.html",
            {
                "stock":stock,
                "live":live,
                "chart":None,
                "signal":None,
            }
        )


    df = apply_user_indicators(request.user, df)
    
    # print(df.columns.tolist())    
    selected = UserIndicator.objects.filter(
    user=request.user,
    enabled=True
)

    signal=None

    if len(df)>=100:
        indicators = {}
        # selected = UserIndicator.objects.filter(
        #     user=request.user,
        #     enabled=True
        #     )
        for item in selected:
            column = f"{item.indicator}{item.period}"
            if column in df.columns:
                indicators[column] = df[column].iloc[-1]
                indicators["volume"] = df["volume"].iloc[-1]
                indicators["avg_volume"] = df["volume"].tail(20).mean()


        signal=generate_signal(
            stock=stock,
            live_price=live["price"],
            indicators=indicators
        )



    fig=make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.70,0.15,0.15]
    )


    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price"
        ),
        row=1,
        col=1
    )
    for item in selected:
        if item.indicator in ["EMA", "SMA"]:
            column = f"{item.indicator}{item.period}"
            if column in df.columns:
                fig.add_trace(

                go.Scatter(
                    x=df["date"],
                    y=df[column],
                    name=column
                ),

                row=1,
                col=1
            )




    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["volume"],
            name="Volume"
        ),
        row=2,
        col=1
    )
    for item in selected:
        if item.indicator == "RSI":
            column = f"RSI{item.period}"
            if column in df.columns:
                fig.add_trace(

                go.Scatter(
                    x=df["date"],
                    y=df[column],
                    name=column
                ),

                row=3,
                col=1
            )




    fig.add_hline(
        y=70,
        line_dash="dash",
        row=3,
        col=1
    )


    fig.add_hline(
        y=30,
        line_dash="dash",
        row=3,
        col=1
    )


    fig.update_layout(
        title=f"{stock.company_name} ({stock.symbol})",
        height=900,
        template="plotly_white",
        xaxis_rangeslider_visible=False
    )


    chart=plot(
        fig,
        output_type="div"
    )


    form = UserIndicatorForm()

    selected = UserIndicator.objects.filter(
    user=request.user,
    enabled=True
    )


    return render(
        request,
        "stocks/stock_detail.html",
        {
            "stock":stock,
            "live":live,
            "chart":chart,
            "signal":signal,
            "form":form,
            "indicators":selected,

        }
    )




@login_required
def stock_create_from_search(request, symbol):
    master = get_object_or_404(
        StockMaster,
        symbol=symbol.upper()
    )

    stock, created = Stock.objects.get_or_create(
        symbol=master.symbol,
        defaults={
            "company_name": master.company_name,
            "exchange": master.exchange,
            "sector": "Unknown",
            "industry": "",

        }

    )

    if created:
        try:
            import_stock_data(stock.symbol)
        except Exception as e:
            print(e)

    return redirect("stock_detail",pk=stock.id)






@login_required
def add_chart_indicator(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)

    if request.method == "POST":
        form = UserIndicatorForm(request.POST)

        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.user = request.user
            indicator.save()

    return redirect("stock_detail", pk=stock.id)


@login_required
def edit_chart_indicator(request, stock_id, pk):
    indicator = get_object_or_404(
        UserIndicator,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = UserIndicatorForm(
            request.POST,
            instance=indicator,
        )

        if form.is_valid():
            form.save()
            return redirect("stock_detail", pk=stock_id)
    else:
        form = UserIndicatorForm(instance=indicator)
    return render(request,"indicators/edit_indicator.html",{"form": form,},)


@login_required
def delete_chart_indicator(request, stock_id, pk):
    indicator = get_object_or_404(
        UserIndicator,
        pk=pk,
        user=request.user,
    )
    indicator.delete()

    return redirect("stock_detail",pk=stock_id,)





# @login_required
# def stock_view(request, symbol):

#     master = get_object_or_404(
#         StockMaster,
#         symbol=symbol.upper()
#     )

#     stock = Stock.objects.filter(
#         symbol=master.symbol
#     ).first()

#     if stock:
#         return redirect("stock_detail", pk=stock.id)

#     return render(
#         request,
#         "stocks/stock_preview.html",
#         {
#             "stock": master,
#             "live": get_live_stock_data(master.symbol),
#         }
#     )


