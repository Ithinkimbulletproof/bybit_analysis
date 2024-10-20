from django import forms
from .models import CurrencyPair, Strategy


class CurrencyPairForm(forms.ModelForm):
    class Meta:
        model = CurrencyPair
        fields = ["name", "current_price", "historical_prices", "volatility"]


class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ["name", "description", "parameters"]
