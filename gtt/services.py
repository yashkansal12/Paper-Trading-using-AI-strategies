from stocks.service import get_live_stock_data
from trading.services import buy_stock
from .models import GTTOrder
from django.utils import timezone


def check_gtt_orders():
    orders = GTTOrder.objects.filter(status="ACTIVE")
    for order in orders:
        live = get_live_stock_data(order.stock.symbol)
        if not live:
            continue
        price = live["price"]
        if price <= order.trigger_price:
            buy_stock(
                order.user,
                order.stock,
                order.quantity,
                price
            )

            order.status = "TRIGGERED"
            order.triggered_at = timezone.now()
            order.save()