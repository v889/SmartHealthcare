# Generated by Django 4.0.2 on 2023-05-01 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0017_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='verify',
            field=models.BooleanField(default=False),
        ),
    ]
