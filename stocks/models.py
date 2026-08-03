from django.db import models


class StockMaster(models.Model):
    EXCHANGE_CHOICES = (
        ("NSE", "NSE"),
        ("BSE", "BSE"),
    )

    symbol = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=200)
    exchange = models.CharField(
        max_length=10,
        choices=EXCHANGE_CHOICES,
        default="NSE",
    )

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} - {self.company_name}"


class Stock(models.Model):
    EXCHANGE_CHOICES = (
        ("NSE", "NSE"),
        ("BSE", "BSE"),
    )

    symbol = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=200)

    exchange = models.CharField(
        max_length=10,
        choices=EXCHANGE_CHOICES,
        default="NSE",
    )

    sector = models.CharField(max_length=100, default="Unknown")
    industry = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} - {self.company_name}"