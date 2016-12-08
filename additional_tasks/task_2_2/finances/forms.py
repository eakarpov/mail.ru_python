from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django import forms

from .models import Charge, Account


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email"
        ]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password"
        ]

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_query = User.objects.filter(username=username)

        if user_query.count() == 0:
            self.add_error("username", "There is no such user!")
        else:
            user = user_query.get()
            if not user.check_password(password):
                self.add_error("password", "Password is not correct!")

        return self.cleaned_data


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "number"
        ]


class AccountLookForForm(forms.Form):
    number = forms.CharField(
        max_length=12,
        min_length=12
    )

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        account = Account.objects.filter(number=number)
        if account is not None:
            return cleaned_data
        else:
            self.add_error("number", "There is no such object in database!")
        return cleaned_data


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ("value", "date")

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