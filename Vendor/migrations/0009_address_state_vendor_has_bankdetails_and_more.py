# Generated by Django 4.0.2 on 2023-02-18 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0008_bank_details_address_building_number_address_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default=None, max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='has_bankdetails',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendor',
            name='has_shopdetails',
            field=models.BooleanField(default=False),
        ),
    ]
