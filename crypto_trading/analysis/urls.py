from django.urls import path
from . import views

urlpatterns = [
    path("<str:symbol>/", views.analyze_view, name="analyze_coin"),
]
