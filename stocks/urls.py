from django.urls import path
from . import views

urlpatterns = [
    path("", views.stock_list, name="stock_list"),
    path("<int:pk>/", views.stock_detail, name="stock_detail"),
    path("search/",views.search_stock,name="search_stock"),
    path("create/<str:symbol>/",views.stock_create_from_search,name="stock_create_from_search"),
    # path("view/<str:symbol>/",views.stock_view,name="stock_view",), 
    path("<int:stock_id>/indicator/",views.add_chart_indicator,name="add_chart_indicator",),  
    path("<int:stock_id>/indicator/<int:pk>/edit/",views.edit_chart_indicator,name="edit_chart_indicator",),
    path("<int:stock_id>/indicator/<int:pk>/delete/",views.delete_chart_indicator,name="delete_chart_indicator",),
]