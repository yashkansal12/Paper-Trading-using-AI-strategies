from django.contrib import admin
from .models import StockPrice


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):

    list_display = (
        "stock",
        "date",
        "close",
        "volume",
    )

    search_fields = (
        "stock__symbol",
    )

    list_filter = (
        "date",
    )