from django.db import models
from django.db.models import Sum

from clearing.core.models import UUIDModel, TimestampedModel
from clearing.companies.models import Company



FUNDS_TYPE_CHOICES = (
    ('INCOMING', 'Входящие средства'),
    ('OUTGOING', 'Исходящие средства'),
    ('HOLDING', 'Замороженные средства'),
    ('LOCKED', 'Заблокированные средства')
)


class Fund(UUIDModel, TimestampedModel):
    type   = models.CharField(max_length=32, choices=FUNDS_TYPE_CHOICES)
    amount = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    is_active = models.BooleanField(default=True)


class Wallet(UUIDModel, TimestampedModel):
    trader: Company         = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='wallet')
    account_number: str     = models.CharField(max_length=32)
    currency_code: str      = models.CharField(max_length=3, default='KZT')
    deposited_amount: str   = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    holding_amount: float   = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    locked_amount: float    = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    available_amount: float = models.DecimalField(default=0, max_digits=32, decimal_places=2)

    funds: Fund = models.ManyToManyField(Fund, blank=True)


    def calculate(self):
        incoming = self.funds.filter(type='INCOMING').aggregate(total=Sum("amount"))['total']
        outgoing = self.funds.filter(type='OUTGOING').aggregate(total=Sum("amount"))['total']
        self.deposited_amount = incoming - outgoing
        self.available_amount = self.deposited_amount
        self.save()
