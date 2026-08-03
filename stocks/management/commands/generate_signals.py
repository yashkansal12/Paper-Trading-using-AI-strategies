from django.core.management.base import BaseCommand
from signals.services import generate_all_signals


class Command(BaseCommand):
    help = "Generate Signals"

    def handle(self, *args, **kwargs):
        generate_all_signals()
        self.stdout.write(
            self.style.SUCCESS("Signals Generated Successfully.")
        )