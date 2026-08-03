from django import forms
from .models import GTTOrder


class GTTOrderForm(forms.ModelForm):
    class Meta:
        model = GTTOrder
        fields = [
            "order_type",
            "trigger_price",
            "quantity",
            "target_price",
            "stop_loss",
            "expiry_date",
        ]

        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
        }