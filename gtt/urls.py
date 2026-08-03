from django.urls import path
from . import views

urlpatterns = [
    path("", views.gtt_list, name="gtt_list"),
    path("create/<int:pk>/", views.create_gtt, name="create_gtt"),
    path("edit/<int:pk>/", views.edit_gtt, name="edit_gtt"),\
    path("cancel/<int:pk>/", views.cancel_gtt, name="cancel_gtt"),
]