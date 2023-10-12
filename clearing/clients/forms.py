from django import forms

from .models import Client, BankAccount


CLIENT_TYPE_CHOICES = (
    ('--', '--'),
    ('TRADER', 'Брокер'),
    ('DEALER', 'Дилер'),
    ('CLIENT', 'Клиент'),
)


COUNTRY_CHOICES = (
    ('--', '--'),
    ('KAZAKHSTAN', 'Казахстан'),
    ('RUSSIA', 'Россия'),
)


class ClientForm(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(choices=COUNTRY_CHOICES))
    postal_code = forms.CharField()
    address = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    person = forms.CharField()
    class Meta:
        model = Client
        fields = ["type", "legal_form", "name", "bin", "country", "postal_code", "address", "email", "phone", "person"]
        widgets = {
            "type": forms.Select(choices=CLIENT_TYPE_CHOICES),
            "email": forms.EmailInput(),
        }


BANK_ACCOUNT_TYPE_CHOICES = (
    ('--', '--'),
    ('MAIN', 'Основной'),
    ('CLEARING', 'Клиринговый'),
)


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["type", "bank_name", "bank_address", "bic", "iban"]
        widgets = {
            "type": forms.Select(choices=BANK_ACCOUNT_TYPE_CHOICES),
        }

