from django import forms


class BacktestForm(forms.Form):

    STRATEGIES = [
    ("ema", "EMA Crossover"),
    ("sma", "SMA Crossover"),
    ("rsi", "RSI"),
    ("macd", "MACD"),
    ("volume", "Volume"),
    ("vwap", "VWAP"),
]

    strategy = forms.ChoiceField(
        choices=STRATEGIES
    )

    initial_capital = forms.DecimalField(
        initial=100000,
        min_value=1000
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    universe = forms.ChoiceField(
        choices=[
            ("db", "Database Stocks"),
            ("custom", "Custom Symbols"),
        ]
    )

    symbols = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )