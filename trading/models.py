from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock


class Trade(models.Model):

    BUY = "BUY"
    SELL = "SELL"

    TRADE_TYPES = (
        (BUY, "Buy"),
        (SELL, "Sell"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE
    )

    trade_type = models.CharField(
        max_length=4,
        choices=TRADE_TYPES
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} {self.trade_type} {self.stock.symbol}"


# class Trade(models.Model):

#     STATUS = (
#         ("OPEN", "Open"),
#         ("CLOSED", "Closed"),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

#     quantity = models.PositiveIntegerField()

#     entry_price = models.DecimalField(max_digits=12, decimal_places=2)

#     exit_price = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         null=True,
#         blank=True,
#     )

#     entry_date = models.DateTimeField(auto_now_add=True)

#     exit_date = models.DateTimeField(
#         null=True,
#         blank=True,
#     )

#     profit = models.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         default=0,
#     )

#     status = models.CharField(
#         max_length=10,
#         choices=STATUS,
#         default="OPEN",
#     )