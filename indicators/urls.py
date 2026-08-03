from django.urls import path
from . import views

urlpatterns = [
    path("", views.indicator_list, name="indicator_list"),
    path("add/", views.add_indicator, name="add_indicator"),
    path("edit/<int:pk>/", views.edit_indicator, name="edit_indicator"),
    path("delete/<int:pk>/", views.delete_indicator, name="delete_indicator"),
]