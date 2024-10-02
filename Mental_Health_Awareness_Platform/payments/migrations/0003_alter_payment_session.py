# Generated by Django 5.1.1 on 2024-10-02 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_payment_payment_status_payment_date_and_more'),
        ('therapy_sessions', '0002_remove_session_client_remove_session_therapist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapy_sessions.therapysession'),
        ),
    ]
