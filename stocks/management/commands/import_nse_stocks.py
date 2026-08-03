import csv
import requests

from django.core.management.base import BaseCommand
from stocks.models import StockMaster


class Command(BaseCommand):
    help = "Import NSE Listed Stocks"

    def handle(self, *args, **kwargs):

        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        rows = csv.DictReader(
            response.text.splitlines()
        )

        count = 0

        for row in rows:

            symbol = row["SYMBOL"].strip()
            company = row["NAME OF COMPANY"].strip()

            StockMaster.objects.update_or_create(

                symbol=symbol,

                defaults={
                    "company_name": company,
                    "exchange": "NSE",
                }

            )

            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} Stocks Imported Successfully."
            )
        )