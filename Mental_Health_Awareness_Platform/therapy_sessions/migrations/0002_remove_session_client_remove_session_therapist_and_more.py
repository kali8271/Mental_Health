# Generated by Django 5.1.1 on 2024-10-02 09:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapy_sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='client',
        ),
        migrations.RemoveField(
            model_name='session',
            name='therapist',
        ),
        migrations.CreateModel(
            name='TherapySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_date', models.DateTimeField()),
                ('session_duration', models.IntegerField(help_text='Duration in minutes')),
                ('booked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_sessions', to=settings.AUTH_USER_MODEL)),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='therapist_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-session_date'],
            },
        ),
    ]
