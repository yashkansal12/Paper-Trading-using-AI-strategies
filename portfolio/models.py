from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock



class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user","stock",)

    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol}"


class Portfolio(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    cash_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=100000
    )

    invested_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    portfolio_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    total_pnl = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.user.username


class Position(models.Model):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="positions"
    )

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=0)

    average_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    current_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    market_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    unrealized_pnl = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.stock.symbol