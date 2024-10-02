from django.shortcuts import render
from .models import Coin
from .utils import analyze_coin

def analyze_view(request, symbol):
    # Получаем настройки и результаты анализа через utils.analyze_coin
    settings, analysis = analyze_coin(symbol)

    # Сохраняем или обновляем информацию о монете в базе данных
    coin, created = Coin.objects.get_or_create(symbol=symbol)
    coin.settings = settings  # Настройки для автотрейдинга
    coin.analysis_result = analysis.to_html()  # Преобразуем DataFrame в HTML для отображения в шаблоне
    coin.save()

    # Отправляем результат в шаблон для отображения
    return render(request, "analysis/result.html", {"coin": coin})
