from django.urls import path
from . import views

urlpatterns = [
    path('analyze/<str:symbol>/', views.analyze_coin, name='analyze_coin'),
]