from django import forms
from .models import UserIndicator


class UserIndicatorForm(forms.ModelForm):
    class Meta:
        model = UserIndicator
        fields = ["indicator", "period"]