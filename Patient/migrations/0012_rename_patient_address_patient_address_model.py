# Generated by Django 4.0.2 on 2023-03-23 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0011_rename_address_patient_address'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Patient_Address',
            new_name='Patient_Address_Model',
        ),
    ]
