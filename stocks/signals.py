from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Stock
from market_data.services import import_stock_data


# @receiver(post_save, sender=Stock)
# def auto_import_history(sender, instance, created, **kwargs):
#     if created:
#         import_stock_data(instance.symbol)