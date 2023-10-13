from django import forms

from .models import Company, BankAccount


COMPANY_TYPE_CHOICES = (
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


class CompanyForm(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(choices=COUNTRY_CHOICES))
    postal_code = forms.CharField()
    address = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    person = forms.CharField()
    class Meta:
        model = Company
        fields = ["type", "legal_form", "name", "bin", "country", "postal_code", "address", "email", "phone", "person"]
        widgets = {
            "type": forms.Select(choices=COMPANY_TYPE_CHOICES),
            "email": forms.EmailInput(),
        }

        



class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["bank_name", "bank_address", "bic", "iban"]
        widgets = {
            
        }

