from django.db import models
from django.db.models import Sum

from clearing.core.models import UUIDModel, TimestampedModel
from clearing.companies.models import Company


FUNDS_PLATFORM_CHOICES = (
    ('DVA', 'DVA'),
    ('STD', 'STD'),
)


FUNDS_TYPE_CHOICES = (
    ('INCOMING', 'Входящие средства'),
    ('OUTGOING', 'Исходящие средства'),
    ('HOLDING', 'Замороженные средства'),
    ('LOCKED', 'Заблокированные средства')
)

FUND_PAYMENT_TYPE_CHOICES = (
    ('BANK_TRANSFER', 'Безналичный перевод'),
    ('CASH_PAYMENT', 'Наличные')
)


class Fund(UUIDModel, TimestampedModel):
    platform: str = models.CharField(max_length=32, choices=FUNDS_PLATFORM_CHOICES, default='DVA')
    type: str  = models.CharField(max_length=32, choices=FUNDS_TYPE_CHOICES)
    amount:float = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    is_active: bool = models.BooleanField(default=True)
    payment_type: str = models.CharField(max_length=32, choices=FUND_PAYMENT_TYPE_CHOICES, default='BANK_TRANSFER')
    payment_number: str = models.TextField(null=True)
    comment: str = models.TextField(null=True)


class Wallet(UUIDModel, TimestampedModel):
    trader: Company         = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='wallet')
    account_number: str     = models.CharField(max_length=32)
    contract_number: str    = models.CharField(max_length=512, null=True)
    currency_code: str      = models.CharField(max_length=3, default='KZT')
    deposited_amount: str   = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    holding_amount: float   = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    locked_amount: float    = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    available_amount: float = models.DecimalField(default=0, max_digits=32, decimal_places=2)

    funds: Fund = models.ManyToManyField(Fund, blank=True)


    def calculate(self):
        query = self.funds.filter(is_active=True)
        incoming = query.filter(type='INCOMING').aggregate(total=Sum("amount"))['total'] or 0
        outgoing = query.filter(type='OUTGOING').aggregate(total=Sum("amount"))['total'] or 0
        holding = query.filter(type='HOLDING').aggregate(total=Sum("amount"))['total'] or 0
        locked = query.filter(type='LOCKED').aggregate(total=Sum("amount"))['total'] or 0
        self.deposited_amount = incoming - outgoing
        self.holding_amount = holding
        self.locked_amount = locked
        self.available_amount = self.deposited_amount - holding - locked
        self.save()


