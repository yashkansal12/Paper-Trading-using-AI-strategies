from django.db import models
from stocks.models import Stock


class Signal(models.Model):

    SIGNAL_CHOICES = [
        ("STRONG BUY", "STRONG BUY"),
        ("BUY", "BUY"),
        ("WATCH", "WATCH"),
        ("HOLD", "HOLD"),
        ("AVOID", "AVOID"),
    ]

    TREND_CHOICES = [
        ("Bullish", "Bullish"),
        ("Bearish", "Bearish"),
        ("Sideways", "Sideways"),
    ]

    stock = models.OneToOneField(Stock,on_delete=models.CASCADE,related_name="signal")
    signal = models.CharField(max_length=20,choices=SIGNAL_CHOICES,default="HOLD",)
    score = models.PositiveIntegerField(default=0)
    confidence = models.PositiveIntegerField(default=0)
    trend = models.CharField(max_length=20,choices=TREND_CHOICES,default="Sideways",)
    entry_price = models.DecimalField(max_digits=10,decimal_places=2,)
    target_price = models.DecimalField(max_digits=10,decimal_places=2,)
    stop_loss = models.DecimalField(max_digits=10,decimal_places=2,)
    risk_reward = models.DecimalField(max_digits=5,decimal_places=2,)
    reason = models.TextField(blank=True,default="",)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

   
    # Indicator values
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ema20 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ema50 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ema200 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    rsi = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    volume = models.BigIntegerField(default=0)

    # Score Breakdown
    trend_score = models.PositiveSmallIntegerField(default=0)
    ema_score = models.PositiveSmallIntegerField(default=0)
    rsi_score = models.PositiveSmallIntegerField(default=0)
    volume_score = models.PositiveSmallIntegerField(default=0)
    rr_score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-score", "-created_at"]
        verbose_name = "Signal"
        verbose_name_plural = "Signals"

    def __str__(self):
        return f"{self.stock.symbol} - {self.signal} ({self.score})"