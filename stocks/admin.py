from django.contrib import admin
from .models import Stock
from market_data.services import import_stock_data


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "company_name",
        "exchange",
        "sector",
        "is_active",
    )

    search_fields = ("symbol", "company_name")
    list_filter = ("exchange", "sector", "is_active")

    def save_model(self, request, obj, form, change):
        print("===== save_model called =====")
        print("change =", change)
        print("symbol =", obj.symbol)

        super().save_model(request, obj, form, change)

        if not change:
            print("Calling import_stock_data...")
            import_stock_data(obj.symbol)
            print("Import completed.")
# Sirf naya stock add hone par history import karo
        if not change:
            try:
                import_stock_data(obj.symbol)
                self.message_user(
                    request,
                    f"{obj.symbol} historical data imported successfully."
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Import failed: {e}",
                    level=messages.ERROR,
                )