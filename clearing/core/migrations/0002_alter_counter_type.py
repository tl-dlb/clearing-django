# Generated by Django 4.2.5 on 2023-10-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='type',
            field=models.CharField(choices=[('MAIN_WALLET', 'Основной счет')], max_length=12),
        ),
    ]
