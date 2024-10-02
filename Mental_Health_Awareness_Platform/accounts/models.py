from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    ROLES = (
        ('client', 'Client'),
        ('therapist', 'Therapist'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username