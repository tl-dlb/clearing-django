from datetime import datetime

from django.db import models


STATUS_CHOICES = (
    ('SEND_CODE', 'SEND_CODE'),
)


METHOD_CHOICES = (
    ('telegram', 'telegram'),
)


class Event(models.Model):
    address: str         = models.CharField(max_length=70)
    event: str           = models.CharField(max_length=12)
    status: str          = models.CharField(max_length=12, choices=STATUS_CHOICES)
    method: str          = models.CharField(max_length=12, choices=METHOD_CHOICES)
    code: int            = models.IntegerField()
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    expired_at: datetime = models.DateTimeField()
    embeded: bool        = models.BooleanField(default=False)
    cert: str            = models.TextField()

    
