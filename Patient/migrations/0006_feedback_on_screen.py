# Generated by Django 4.0.2 on 2023-02-22 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0005_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='on_screen',
            field=models.BooleanField(default=False),
        ),
    ]
