from django.urls import path
from . import views

urlpatterns=[
    path("watchlist/add/<int:id>/",views.add_watchlist,name="add_watchlist"),
    path("watchlist/",views.watchlist,name="watchlist"),
    path("",views.portfolio_dashboard,name="portfolio"),
]