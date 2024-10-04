from django.shortcuts import render
from .models import Coin
from .utils import perform_analysis


def analyze_view(request, symbol):
    settings, analysis = perform_analysis(symbol)

    coin, created = Coin.objects.get_or_create(symbol=symbol)
    coin.settings = settings
    coin.analysis_result = analysis.to_html()
    coin.save()

    return render(
        request,
        "analysis/result.html",
        {"coin": coin, "project_name": "Fazanka Records Crypto Trading"},
    )
