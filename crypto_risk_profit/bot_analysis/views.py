from django.shortcuts import render
from .models import CurrencyPair
import requests
import numpy as np

BYBIT_API_URL = "https://api.bybit.com/v2/public"


def fetch_price_data(currency_pair):
    url = f"{BYBIT_API_URL}/kline?symbol={currency_pair}&interval=1&limit=30"
    response = requests.get(url)
    data = response.json()
    return [float(candle[4]) for candle in data["result"]]


def calculate_risk(prices):
    if len(prices) > 1:
        return np.std(prices)
    return 0


def index(request):
    currency_pairs = ["BTCUSDT", "ETHUSDT"]
    for pair in currency_pairs:
        historical_prices = fetch_price_data(pair)
        volatility = calculate_risk(historical_prices)
        current_price = historical_prices[-1] if historical_prices else 0
        CurrencyPair.objects.update_or_create(
            name=pair,
            defaults={
                "current_price": current_price,
                "historical_prices": historical_prices,
                "volatility": volatility,
            },
        )
    pairs = CurrencyPair.objects.all()
    return render(request, "index.html", {"currency_pairs": pairs})
