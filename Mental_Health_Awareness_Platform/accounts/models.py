from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    ROLES = (
        ('client', 'Client'),
        ('therapist', 'Therapist'),
    )

    role = models.CharField(max_length=10, choices=ROLES, default='client')
    bio = models.TextField(blank=True, null=True)
    client_photo = models.ImageField(upload_to='client_photos', blank=True, null=True)
    therapist_photo = models.ImageField(upload_to='therapist_photos', blank=True, null=True)

    def __str__(self):
        if self.role == 'therapist' and self.therapist_photo:
            return f'{self.username} (Therapist, {self.therapist_photo.url})'
        elif self.role == 'client' and self.client_photo:
            return f'{self.username} (Client, {self.client_photo.url})'
        return self.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
