from django.db import models
from django.contrib.auth.models import User


class UserIndicator(models.Model):

    INDICATORS = [
        ("EMA", "EMA"),
        ("SMA", "SMA"),
        ("RSI", "RSI"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    indicator = models.CharField(
        max_length=20,
        choices=INDICATORS
    )

    period = models.PositiveIntegerField()

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.indicator} {self.period}"