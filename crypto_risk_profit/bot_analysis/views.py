from django.shortcuts import render, redirect, get_object_or_404
from .models import CurrencyPair, Strategy
from .forms import CurrencyPairForm, StrategyForm
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


def pair_analysis(request, currency_pair):
    pair = get_object_or_404(CurrencyPair, name=currency_pair)
    return render(request, "pair_analysis.html", {"pair": pair})


def add_pair(request):
    if request.method == "POST":
        form = CurrencyPairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = CurrencyPairForm()
    return render(request, "add_pair.html", {"form": form})


def delete_pair(request, currency_pair):
    pair = get_object_or_404(CurrencyPair, name=currency_pair)
    pair.delete()
    return redirect("index")


def update_pair(request, currency_pair):
    pair = get_object_or_404(CurrencyPair, name=currency_pair)
    historical_prices = fetch_price_data(pair.name)
    pair.current_price = historical_prices[-1] if historical_prices else 0
    pair.volatility = calculate_risk(historical_prices)
    pair.historical_prices = historical_prices
    pair.save()
    return redirect("pair_analysis", currency_pair=currency_pair)


def add_strategy(request):
    if request.method == "POST":
        form = StrategyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = StrategyForm()
    return render(request, "add_strategy.html", {"form": form})
