# Generated by Django 4.0.2 on 2023-02-19 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0010_bank_details_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='Vendor.vendor'),
            preserve_default=False,
        ),
    ]
