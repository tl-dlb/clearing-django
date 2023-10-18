import uuid
from datetime import datetime

from django.db import models


class TimestampedModel(models.Model):
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class UUIDModel(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

    class Meta:
        abstract = True


COUNTER_TYPE_CHOICES = (
    ('MAIN_WALLET', 'Основной счет'),
)

class Counter(models.Model):
    type: str = models.CharField(max_length=12, choices=COUNTER_TYPE_CHOICES)
    value: int = models.IntegerField(default=0)