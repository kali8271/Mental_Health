from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    ROLES = (
        ('client', 'Client'),
        ('therapist', 'Therapist'),
    )
    
    # Role of the user (client or therapist)
    role = models.CharField(max_length=10, choices=ROLES)
    
    # Additional fields for user profile
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)  # Add profile picture field if needed

    def __str__(self):
        return self.username  # Return the username for easy identification in admin panel

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
