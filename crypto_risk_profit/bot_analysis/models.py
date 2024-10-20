from django.db import models


class CurrencyPair(models.Model):
    name = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=20, decimal_places=10)
    historical_prices = models.JSONField()
    volatility = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Strategy(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    parameters = models.JSONField()

    def __str__(self):
        return self.name
