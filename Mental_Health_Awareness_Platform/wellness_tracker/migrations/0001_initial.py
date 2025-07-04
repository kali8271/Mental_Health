# Generated by Django 5.2.3 on 2025-06-28 19:28

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WellnessGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('goal_type', models.CharField(choices=[('mood', 'Mood Improvement'), ('sleep', 'Sleep Quality'), ('exercise', 'Physical Activity'), ('social', 'Social Connection'), ('stress', 'Stress Management'), ('self_care', 'Self Care'), ('therapy', 'Therapy Goals'), ('custom', 'Custom Goal')], max_length=20)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=10)),
                ('target_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('current_value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('unit', models.CharField(blank=True, max_length=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('target_date', models.DateField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wellness_goals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wellness Goal',
                'verbose_name_plural': 'Wellness Goals',
                'ordering': ['-priority', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WellnessReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('reminder_type', models.CharField(choices=[('reflection', 'Daily Reflection'), ('meditation', 'Meditation'), ('exercise', 'Exercise'), ('medication', 'Medication'), ('therapy', 'Therapy Session'), ('self_care', 'Self Care'), ('custom', 'Custom Reminder')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('time', models.TimeField()),
                ('days_of_week', models.JSONField(default=list)),
                ('is_active', models.BooleanField(default=True)),
                ('notification_method', models.CharField(choices=[('email', 'Email'), ('push', 'Push Notification')], default='push', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wellness_reminders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wellness Reminder',
                'verbose_name_plural': 'Wellness Reminders',
                'ordering': ['time'],
            },
        ),
        migrations.CreateModel(
            name='WellnessReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('report_data', models.JSONField(default=dict)),
                ('insights', models.JSONField(default=list)),
                ('recommendations', models.JSONField(default=list)),
                ('is_generated', models.BooleanField(default=False)),
                ('generated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wellness_reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wellness Report',
                'verbose_name_plural': 'Wellness Reports',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MoodPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('morning_mood', models.IntegerField(blank=True, choices=[(1, 'Very Sad'), (2, 'Sad'), (3, 'Neutral'), (4, 'Happy'), (5, 'Very Happy')], null=True)),
                ('afternoon_mood', models.IntegerField(blank=True, choices=[(1, 'Very Sad'), (2, 'Sad'), (3, 'Neutral'), (4, 'Happy'), (5, 'Very Happy')], null=True)),
                ('evening_mood', models.IntegerField(blank=True, choices=[(1, 'Very Sad'), (2, 'Sad'), (3, 'Neutral'), (4, 'Happy'), (5, 'Very Happy')], null=True)),
                ('positive_factors', models.JSONField(default=list)),
                ('negative_factors', models.JSONField(default=list)),
                ('weather_condition', models.CharField(blank=True, max_length=50)),
                ('temperature', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mood_patterns', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mood Pattern',
                'verbose_name_plural': 'Mood Patterns',
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Reflection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('mood_rating', models.IntegerField(choices=[(1, 'Very Sad'), (2, 'Sad'), (3, 'Neutral'), (4, 'Happy'), (5, 'Very Happy')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('anxiety_level', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Moderate'), (4, 'High'), (5, 'Very High')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('stress_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('sleep_hours', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('sleep_quality', models.IntegerField(blank=True, choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Fair'), (4, 'Good'), (5, 'Excellent')], null=True)),
                ('exercise_minutes', models.PositiveIntegerField(default=0)),
                ('water_intake_glasses', models.PositiveIntegerField(default=0)),
                ('activities_completed', models.JSONField(default=list)),
                ('habits_tracked', models.JSONField(default=dict)),
                ('reflection_text', models.TextField(blank=True)),
                ('gratitude_entries', models.JSONField(default=list)),
                ('challenges_faced', models.TextField(blank=True)),
                ('coping_strategies', models.TextField(blank=True)),
                ('daily_goals', models.JSONField(default=list)),
                ('goals_achieved', models.JSONField(default=list)),
                ('social_interactions', models.PositiveIntegerField(default=0)),
                ('support_received', models.BooleanField(default=False)),
                ('support_provided', models.BooleanField(default=False)),
                ('medication_taken', models.BooleanField(default=False)),
                ('therapy_session', models.BooleanField(default=False)),
                ('self_care_activities', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reflections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reflection',
                'verbose_name_plural': 'Reflections',
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
        migrations.CreateModel(
            name='WellnessStreak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streak_type', models.CharField(max_length=50)),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('longest_streak', models.PositiveIntegerField(default=0)),
                ('last_activity_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wellness_streaks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wellness Streak',
                'verbose_name_plural': 'Wellness Streaks',
                'unique_together': {('user', 'streak_type')},
            },
        ),
    ]
