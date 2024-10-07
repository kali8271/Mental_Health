# Generated by Django 5.1.1 on 2024-10-07 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('therapist', 'Therapist')], max_length=10),
        ),
    ]
