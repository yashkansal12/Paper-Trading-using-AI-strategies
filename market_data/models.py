from django.db import models
from stocks.models import Stock


class StockPrice(models.Model):

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="prices",
    )

    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("stock", "date")
        ordering = ["-date"]
    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"