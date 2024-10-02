from django.db import models


class Coin(models.Model):
    symbol = models.CharField(max_length=10)  # символ монеты (например, BTCUSDT)
    settings = models.JSONField(null=True, blank=True)  # настройки для автотрейдинга
    analysis_result = models.TextField(null=True, blank=True)  # результат анализа

    def __str__(self):
        return self.symbol
