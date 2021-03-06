from datetime import date
from decimal import Decimal

from django import forms

from .models import Charge


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = [
            "value",
            "date"
        ]

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('value')
        charge_date = cleaned_data.get('date')
        if value is None or date is None:
            return cleaned_data
        if value == Decimal(0):
            self.add_error("value", "Charge can't be a zero value")
        if value < 0 and charge_date > date.today():
            self.add_error("date", "You can't set negative charge on future day")
        return cleaned_data
