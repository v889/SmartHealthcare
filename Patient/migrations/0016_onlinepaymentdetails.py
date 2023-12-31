# Generated by Django 4.0.2 on 2023-04-01 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0015_rename_quantity_order_number_of_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlinePaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_order_paymnet', to='Patient.order')),
            ],
        ),
    ]
