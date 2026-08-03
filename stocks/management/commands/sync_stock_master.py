from django.core.management.base import BaseCommand
from stocks.models import StockMaster, Stock


class Command(BaseCommand):
    help = "Sync StockMaster to Stock"

    def handle(self, *args, **kwargs):

        count = 0

        for master in StockMaster.objects.all():

            Stock.objects.update_or_create(
                symbol=master.symbol,
                defaults={
                    "company_name": master.company_name,
                    "exchange": master.exchange,
                    "is_active": True,
                },
            )

            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} stocks synced successfully."
            )
        )