# Generated by Django 4.0.2 on 2023-02-16 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=10)),
                ('license_number', models.CharField(max_length=15)),
                ('issue_authority_name', models.CharField(max_length=1000)),
                ('aadhar_card_number', models.CharField(max_length=12)),
                ('is_authorize', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('price', models.IntegerField()),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Vendor.category')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=2000)),
                ('adress1', models.CharField(max_length=2000)),
                ('adress2', models.CharField(max_length=2000)),
                ('zip_code', models.CharField(max_length=2000)),
                ('city', models.CharField(max_length=2000)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_address', to='Vendor.vendor')),
            ],
        ),
    ]
