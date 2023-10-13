from django.db import models

from clearing.core.models import UUIDModel, TimestampedModel
from clearing.companies.models import Company

# Create your models here.
class MainWallet(UUIDModel, TimestampedModel):
    company: Company          = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='wallet')
    account_number: str     = models.CharField(max_length=32, blank=True)
    currency_code: str      = models.CharField(max_length=3, default='KZT')
    deposited_amount: str   = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    holding_amount: float   = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    locked_amount: float    = models.DecimalField(default=0, max_digits=32, decimal_places=2)
    available_amount: float = models.DecimalField(default=0, max_digits=32, decimal_places=2)
