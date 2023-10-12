
from django.db import models

from clearing.core.models import UUIDModel, TimestampedModel


CLIENT_TYPE_CHOICES = (
    ('TRADER', 'Брокер'),
    ('DEALER', 'Дилер'),
    ('CLIENT', 'Клиент'),
)


CLIENT_STATUS_CHOICES = (
    ('REVIEW', 'В обработке'),
    ('ACTIVE', 'Активный'),
    ('BLOCKED', 'Заблокирован'), 
    ('DENIED', 'Отклонен'),
)


INFO_TYPE_CHOICES = (
    ('COUNTRY', 'COUNTRY'),
    ('POSTAL_CODE', 'POSTAL_CODE'),
    ('ADDRESS', 'ADDRESS'),  
    ('EMAIL', 'EMAIL'),
    ('PHONE', 'PHONE'),
    ('PERSON', 'PERSON'), 
)

BANK_ACCOUNT_TYPE_CHOICES = (
    ('MAIN', 'Основной'),
    ('CLEARING', 'Клиринговый'),
)

LEGAL_FORM_CHOICES = (
    ('LLP', 'ТОО'),
    ('JSC', 'АО'),
    ('IE', 'ИП'),
)


class BankAccount(UUIDModel, TimestampedModel):
    type: str         = models.CharField(max_length=12, choices=BANK_ACCOUNT_TYPE_CHOICES, default='DEFAULT')
    bank_name: str    = models.TextField()
    bank_address: str = models.TextField()
    bic: str          = models.CharField(max_length=11)
    iban: str         = models.CharField(max_length=34)


class Info(UUIDModel, TimestampedModel):
    type: str  = models.CharField(max_length=32, choices=INFO_TYPE_CHOICES)
    value: str = models.TextField()


class Client(UUIDModel, TimestampedModel):
    name: str   = models.TextField()
    bin: str    = models.CharField(max_length=12, unique=True, verbose_name='БИН')
    type: str   = models.CharField(max_length=32, choices=CLIENT_TYPE_CHOICES)
    legal_form  = models.CharField(max_length=12, choices=LEGAL_FORM_CHOICES)
    status: str = models.CharField(max_length=32, choices=CLIENT_STATUS_CHOICES, default='REVIEW')

    bank_accounts: BankAccount = models.ManyToManyField(BankAccount, blank=True)
    info: Info                = models.ManyToManyField(Info, blank=True)

    class Meta:
        verbose_name = 'Клиент'

    @property
    def full_name(self):
        return '%s %s' % (self.get_legal_form_display(), self.name)

    @property
    def country(self):
        return self.info.filter(type='COUNTRY').first()
    
    @property
    def postal_code(self):
        return self.info.filter(type='POSTAL_CODE').first()
    
    @property
    def address(self):
        return self.info.filter(type='ADDRESS').first()
    
    @property
    def email(self):
        return self.info.filter(type='EMAIL').first()
    
    @property
    def phone(self):
        return self.info.filter(type='PHONE').first()
    
    @property
    def person(self):
        return self.info.filter(type='PERSON').first()
        