from django.contrib import admin
from .models import Signal


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = (
        "stock",
        "signal",
        "entry_price",
        "target_price",
        "stop_loss",
        "risk_reward",
        "created_at",
    )

    list_filter = (
        "signal",
        "created_at",
    )

    search_fields = (
        "stock__symbol",
        "stock__company_name",
    )