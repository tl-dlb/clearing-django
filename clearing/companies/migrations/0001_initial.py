# Generated by Django 4.2.5 on 2023-10-13 07:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('MAIN', 'Основной'), ('CLEARING', 'Клиринговый')], default='DEFAULT', max_length=12)),
                ('bank_name', models.TextField()),
                ('bank_address', models.TextField()),
                ('bic', models.CharField(max_length=11)),
                ('iban', models.CharField(max_length=34)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('COUNTRY', 'COUNTRY'), ('POSTAL_CODE', 'POSTAL_CODE'), ('ADDRESS', 'ADDRESS'), ('EMAIL', 'EMAIL'), ('PHONE', 'PHONE'), ('PERSON', 'PERSON')], max_length=32)),
                ('value', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('bin', models.CharField(max_length=12, unique=True, verbose_name='БИН')),
                ('type', models.CharField(choices=[('TRADER', 'Брокер'), ('DEALER', 'Дилер'), ('CLIENT', 'Клиент')], max_length=32)),
                ('legal_form', models.CharField(choices=[('LLP', 'ТОО'), ('JSC', 'АО'), ('IE', 'ИП')], max_length=12)),
                ('status', models.CharField(choices=[('REVIEW', 'В обработке'), ('ACTIVE', 'Активный'), ('BLOCKED', 'Заблокирован'), ('DENIED', 'Отклонен')], default='REVIEW', max_length=32)),
                ('bank_accounts', models.ManyToManyField(blank=True, to='companies.bankaccount')),
                ('info', models.ManyToManyField(blank=True, to='companies.info')),
            ],
            options={
                'verbose_name': 'Компания',
            },
        ),
    ]
