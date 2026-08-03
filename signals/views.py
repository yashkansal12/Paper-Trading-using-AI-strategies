from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Signal
from .services import generate_all_signals


@login_required
def signal_list(request):
    """
    Generate latest signals and display them.
    """

    # Generate fresh signals
    
    
    
    
    
    # generate_all_signals()






    # Fetch all signals ordered by score
    signals = (
        Signal.objects
        .select_related("stock")
        .order_by("-score", "stock__symbol")
    )

    context = {
        "signals": signals,
        "total_signals": signals.count(),
        "strong_buy_count": signals.filter(signal="STRONG BUY").count(),
        "buy_count": signals.filter(signal="BUY").count(),
        "watch_count": signals.filter(signal="WATCH").count(),
        "hold_count": signals.filter(signal="HOLD").count(),
        "avoid_count": signals.filter(signal="AVOID").count(),
    }

    return render(request,"signals/signal_list.html",context,)



    # signals = Signal.objects.select_related("stock").order_by("-score")
    # return render(request,"signals/signal_list.html",{"signals": signals})