from django import forms

from .models import Fund


class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ["amount", "payment_type", "payment_number", "comment"]
        widgets = {
            "payment_number": forms.TextInput(),
            "comment": forms.TextInput(),
        }
