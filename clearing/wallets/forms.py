from django import forms
from django.core.exceptions import ValidationError

from .models import Fund


class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ["amount", "payment_type", "payment_number", "comment"]
        widgets = {
            "payment_number": forms.TextInput(),
            "comment": forms.TextInput(),
            "payment_type": forms.RadioSelect(),
        }

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data <= 0:
            raise ValidationError('ValidationError.')
        return data

