from django.urls import path
from . import views

urlpatterns = [
    path("", views.backtest_dashboard, name="backtest_dashboard"),
]