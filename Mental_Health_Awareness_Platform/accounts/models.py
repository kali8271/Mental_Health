from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('therapist', 'Therapist'),
        ('admin', 'Admin'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    # Enhanced user fields
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    
    # Profile information
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    user_timezone = models.CharField(max_length=50, default='UTC')
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    notification_preferences = models.JSONField(default=dict)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Timestamps with default values
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class TherapistProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='therapist_profile')
    
    # Professional information
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=200)
    years_of_experience = models.PositiveIntegerField(default=0)
    education = models.TextField()
    certifications = models.JSONField(default=list)
    
    # Professional photos
    therapist_photo = models.ImageField(upload_to='therapist_photos/', null=True, blank=True)
    license_photo = models.ImageField(upload_to='license_photos/', null=True, blank=True)
    
    # Availability and rates
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    availability_schedule = models.JSONField(default=dict)
    max_clients = models.PositiveIntegerField(default=20)
    
    # Professional details
    languages_spoken = models.JSONField(default=list)
    treatment_approaches = models.JSONField(default=list)
    client_populations = models.JSONField(default=list)
    
    # Verification and status
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_sessions = models.PositiveIntegerField(default=0)
    
    # Timestamps with default values
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Therapist Profile'
        verbose_name_plural = 'Therapist Profiles'
    
    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.specialization}"
    
    @property
    def average_rating(self):
        return round(self.rating, 1) if self.rating > 0 else 0

class ClientProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='client_profile')
    
    # Personal information
    client_photo = models.ImageField(upload_to='client_photos/', null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Health information
    medical_history = models.TextField(blank=True)
    current_medications = models.JSONField(default=list)
    allergies = models.JSONField(default=list)
    
    # Therapy preferences
    preferred_therapy_type = models.CharField(max_length=100, blank=True)
    preferred_gender = models.CharField(max_length=10, blank=True)
    session_duration_preference = models.CharField(max_length=20, default='60min')
    
    # Progress tracking
    therapy_goals = models.JSONField(default=list)
    progress_notes = models.JSONField(default=list)
    
    # Timestamps with default values
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'
    
    def __str__(self):
        return f"{self.user.full_name} (Client)"

class UserSession(models.Model):
    """Track user sessions for analytics and security"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class Notification(models.Model):
    """User notifications system"""
    NOTIFICATION_TYPES = [
        ('session_reminder', 'Session Reminder'),
        ('message', 'New Message'),
        ('payment', 'Payment Update'),
        ('system', 'System Update'),
        ('wellness', 'Wellness Reminder'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
