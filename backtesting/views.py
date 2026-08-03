from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from stocks.models import Stock

from .engine import BacktestEngine
from .forms import BacktestForm


@login_required
def backtest_dashboard(request):

    result = None

    if request.method == "POST":

        form = BacktestForm(request.POST)

        if form.is_valid():

            engine = BacktestEngine(form.cleaned_data)
            result = engine.run()

        else:
            print(form.errors)

    else:

        form = BacktestForm()

    return render(
        request,
        "backtesting/dashboard.html",
        {
            "form": form,
            "result": result,
            "total_stocks": Stock.objects.count(),
        },
    )