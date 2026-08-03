from django.core.management.base import BaseCommand
from gtt.services import check_gtt_orders


class Command(BaseCommand):
    help = "Check and trigger GTT Orders"

    def handle(self, *args, **kwargs):
        check_gtt_orders()
        self.stdout.write(
            self.style.SUCCESS("GTT Orders Checked Successfully")
        )