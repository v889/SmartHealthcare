# Generated by Django 4.0.2 on 2023-03-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0003_doctor_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='fees',
            field=models.DecimalField(decimal_places=3, default=500.0, max_digits=7),
        ),
    ]
