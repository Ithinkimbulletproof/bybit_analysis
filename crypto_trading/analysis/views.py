from django.shortcuts import render
from .models import Coin
from .utils import analyze_coin


def analyze_view(request, symbol):
    settings, analysis = analyze_coin(symbol)

    # Сохраняем результаты в базу данных
    coin, created = Coin.objects.get_or_create(symbol=symbol)
    coin.settings = settings
    coin.analysis_result = analysis.to_html()  # Преобразуем DataFrame в HTML
    coin.save()

    return render(request, "analysis/result.html", {"coin": coin})
