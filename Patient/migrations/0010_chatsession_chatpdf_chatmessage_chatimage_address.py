# Generated by Django 4.0.2 on 2023-03-21 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0004_doctor_fees'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Patient', '0009_patientdocument_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patient.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ChatPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='chat_pdfs')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patient.chatsession')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patient.chatsession')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='chat_images')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patient.chatsession')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=2000)),
                ('last_name', models.CharField(max_length=2000)),
                ('village_or_colony', models.CharField(max_length=2000)),
                ('landmark', models.CharField(max_length=3000)),
                ('Building_Number', models.IntegerField()),
                ('zip_code', models.CharField(max_length=2000)),
                ('city', models.CharField(max_length=2000)),
                ('state', models.CharField(max_length=1024)),
                ('country', models.CharField(max_length=2000)),
                ('phone_number', models.CharField(max_length=10)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_address', to='Patient.patient')),
            ],
        ),
    ]
