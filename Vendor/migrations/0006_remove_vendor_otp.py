# Generated by Django 4.0.2 on 2023-02-17 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0005_alter_vendor_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='otp',
        ),
    ]
