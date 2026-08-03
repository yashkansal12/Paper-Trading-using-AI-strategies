from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock


class GTTOrder(models.Model):

    BUY = "BUY"
    SELL = "SELL"

    STATUS = (
        ("ACTIVE", "Active"),
        ("TRIGGERED", "Triggered"),
        ("EXPIRED", "Expired"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    order_type = models.CharField(
        max_length=4,
        choices=((BUY, "Buy"), (SELL, "Sell"))
    )

    trigger_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="ACTIVE"
    )

    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.stock.symbol} - {self.status}"