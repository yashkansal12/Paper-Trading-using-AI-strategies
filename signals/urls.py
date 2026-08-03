from django.urls import path
from . import views

urlpatterns = [
    path("", views.signal_list, name="signals"),
]