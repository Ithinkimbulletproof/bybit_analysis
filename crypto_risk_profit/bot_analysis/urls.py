from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pair/<str:currency_pair>/", views.pair_analysis, name="pair_analysis"),
    path("add-pair/", views.add_pair, name="add_pair"),
    path("delete-pair/<str:currency_pair>/", views.delete_pair, name="delete_pair"),
    path("update-pair/<str:currency_pair>/", views.update_pair, name="update_pair"),
]
