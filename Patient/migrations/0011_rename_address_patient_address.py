# Generated by Django 4.0.2 on 2023-03-23 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0010_chatsession_chatpdf_chatmessage_chatimage_address'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address',
            new_name='Patient_Address',
        ),
    ]
