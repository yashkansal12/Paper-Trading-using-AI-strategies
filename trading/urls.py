from django.urls import path
from . import views

urlpatterns = [
    path("buy/<int:pk>/",views.buy,name="buy_stock"),
    path("sell/<int:pk>/",views.sell,name="sell_stock",),
    path("", views.trade_history, name="trade_history"),
]