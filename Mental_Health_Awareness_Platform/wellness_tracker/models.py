from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class Reflection(models.Model):
    MOOD_CHOICES = [
        (1, 'Very Sad'),
        (2, 'Sad'),
        (3, 'Neutral'),
        (4, 'Happy'),
        (5, 'Very Happy'),
    ]
    
    ANXIETY_LEVELS = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'High'),
        (5, 'Very High'),
    ]
    
    SLEEP_QUALITY = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Fair'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reflections')
    date = models.DateField(default=timezone.now)
    
    # Mood and emotional tracking
    mood_rating = models.IntegerField(choices=MOOD_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    anxiety_level = models.IntegerField(choices=ANXIETY_LEVELS, validators=[MinValueValidator(1), MaxValueValidator(5)])
    stress_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    # Physical health tracking
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    sleep_quality = models.IntegerField(choices=SLEEP_QUALITY, null=True, blank=True)
    exercise_minutes = models.PositiveIntegerField(default=0)
    water_intake_glasses = models.PositiveIntegerField(default=0)
    
    # Daily activities and habits
    activities_completed = models.JSONField(default=list)  # List of activities done
    habits_tracked = models.JSONField(default=dict)  # Dictionary of habits and their completion status
    
    # Reflection content
    reflection_text = models.TextField(blank=True)
    gratitude_entries = models.JSONField(default=list)  # List of things grateful for
    challenges_faced = models.TextField(blank=True)
    coping_strategies = models.TextField(blank=True)
    
    # Goals and progress
    daily_goals = models.JSONField(default=list)
    goals_achieved = models.JSONField(default=list)
    
    # Social and support
    social_interactions = models.PositiveIntegerField(default=0)
    support_received = models.BooleanField(default=False)
    support_provided = models.BooleanField(default=False)
    
    # Additional tracking
    medication_taken = models.BooleanField(default=False)
    therapy_session = models.BooleanField(default=False)
    self_care_activities = models.JSONField(default=list)
    
    # Metadata with default values
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        verbose_name = 'Reflection'
        verbose_name_plural = 'Reflections'
    
    def __str__(self):
        return f"{self.user.username} - {self.date} (Mood: {self.get_mood_rating_display()})"
    
    @property
    def overall_wellness_score(self):
        """Calculate overall wellness score based on various factors"""
        score = 0
        total_factors = 0
        
        # Mood contributes 30%
        if self.mood_rating:
            score += (self.mood_rating / 5) * 30
            total_factors += 30
        
        # Sleep quality contributes 20%
        if self.sleep_quality:
            score += (self.sleep_quality / 5) * 20
            total_factors += 20
        
        # Exercise contributes 15%
        if self.exercise_minutes:
            exercise_score = min(self.exercise_minutes / 30, 1)  # 30+ minutes = full score
            score += exercise_score * 15
            total_factors += 15
        
        # Social interactions contribute 15%
        social_score = min(self.social_interactions / 5, 1)  # 5+ interactions = full score
        score += social_score * 15
        total_factors += 15
        
        # Stress level (inverse) contributes 20%
        if self.stress_level:
            stress_score = (11 - self.stress_level) / 10  # Lower stress = higher score
            score += stress_score * 20
            total_factors += 20
        
        return round(score / total_factors * 100, 1) if total_factors > 0 else 0

class WellnessGoal(models.Model):
    GOAL_TYPES = [
        ('mood', 'Mood Improvement'),
        ('anxiety', 'Anxiety Reduction'),
        ('sleep', 'Sleep Quality'),
        ('exercise', 'Physical Activity'),
        ('social', 'Social Connection'),
        ('water', 'Hydration'),
        ('meditation', 'Meditation'),
        ('custom', 'Custom Goal'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wellness_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], default='daily')
    
    # Goal tracking
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, help_text="e.g., minutes, glasses, times", blank=True)
    
    # Progress tracking
    start_date = models.DateField(default=timezone.now)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Goal status
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    
    # Timestamps with default values
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = 'Wellness Goal'
        verbose_name_plural = 'Wellness Goals'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage towards goal"""
        if not self.target_value or self.target_value == 0:
            return 0
        progress = (self.current_value / self.target_value) * 100
        return min(progress, 100)
    
    @property
    def is_overdue(self):
        """Check if goal is overdue"""
        if self.target_date and not self.is_completed:
            return timezone.now().date() > self.target_date
        return False

    @property
    def is_completed(self):
        return self.current_value >= self.target_value

class WellnessActivity(models.Model):
    ACTIVITY_TYPES = [
        ('meditation', 'Meditation'),
        ('exercise', 'Exercise'),
        ('reading', 'Reading'),
        ('journaling', 'Journaling'),
        ('social', 'Social Activity'),
        ('hobby', 'Hobby'),
        ('therapy', 'Therapy Session'),
        ('self_care', 'Self Care'),
        ('custom', 'Custom Activity'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    mood_before = models.IntegerField(choices=Reflection.MOOD_CHOICES, null=True, blank=True)
    mood_after = models.IntegerField(choices=Reflection.MOOD_CHOICES, null=True, blank=True)
    energy_level = models.IntegerField(choices=[
        (1, 'Very Low'), (2, 'Low'), (3, 'Moderate'), (4, 'High'), (5, 'Very High')
    ], null=True, blank=True)
    completed = models.BooleanField(default=False)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class MoodAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    average_mood = models.DecimalField(max_digits=3, decimal_places=2)
    mood_entries = models.IntegerField(default=0)
    anxiety_level = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    sleep_quality = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    activity_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    social_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class WellnessStreak(models.Model):
    """Track user streaks for various wellness activities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wellness_streaks')
    streak_type = models.CharField(max_length=20, choices=[
        ('reflection', 'Daily Reflection'),
        ('meditation', 'Meditation'),
        ('exercise', 'Exercise'),
        ('water', 'Water Intake'),
        ('sleep', 'Sleep Goal'),
        ('social', 'Social Activity'),
    ])
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'streak_type']
        verbose_name = 'Wellness Streak'
        verbose_name_plural = 'Wellness Streaks'
    
    def __str__(self):
        return f"{self.user.username} - {self.streak_type} (Streak: {self.current_streak})"

    def update_streak(self, activity_date):
        """Update streak based on activity date"""
        if not self.last_activity_date:
            self.current_streak = 1
            self.last_activity_date = activity_date
        else:
            days_diff = (activity_date - self.last_activity_date).days
            if days_diff == 1:  # Consecutive day
                self.current_streak += 1
            elif days_diff == 0:  # Same day, no change
                pass
            else:  # Streak broken
                self.current_streak = 1
            
            self.last_activity_date = activity_date
        
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.save()

class WellnessReminder(models.Model):
    """Custom reminders for wellness activities"""
    REMINDER_TYPES = [
        ('reflection', 'Daily Reflection'),
        ('meditation', 'Meditation'),
        ('exercise', 'Exercise'),
        ('medication', 'Medication'),
        ('therapy', 'Therapy Session'),
        ('self_care', 'Self Care'),
        ('custom', 'Custom Reminder'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wellness_reminders')
    title = models.CharField(max_length=200)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    description = models.TextField(blank=True)
    
    # Scheduling
    time = models.TimeField()
    days_of_week = models.JSONField(default=list)  # [0,1,2,3,4,5,6] for days of week
    is_active = models.BooleanField(default=True)
    
    # Notification settings
    notification_method = models.CharField(max_length=20, choices=[('email', 'Email'), ('push', 'Push Notification')], default='push')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['time']
        verbose_name = 'Wellness Reminder'
        verbose_name_plural = 'Wellness Reminders'
    
    def __str__(self):
        return f"{self.user.username} - {self.title} at {self.time}"

class WellnessReport(models.Model):
    """Generated wellness reports and insights"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wellness_reports')
    report_type = models.CharField(max_length=50)  # 'weekly', 'monthly', 'custom'
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Report data
    report_data = models.JSONField(default=dict)
    insights = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    
    # Report status
    is_generated = models.BooleanField(default=False)
    generated_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wellness Report'
        verbose_name_plural = 'Wellness Reports'
    
    def __str__(self):
        return f"{self.user.username} - {self.report_type} Report ({self.start_date} to {self.end_date})"
