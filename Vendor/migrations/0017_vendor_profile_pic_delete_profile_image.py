# Generated by Django 4.0.2 on 2023-05-01 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0016_alter_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='profile_pic',
            field=models.ImageField(default='Profile.png', upload_to=''),
        ),
        migrations.DeleteModel(
            name='Profile_Image',
        ),
    ]
