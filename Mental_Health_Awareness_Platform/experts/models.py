# experts/models.py

from django.db import models
from django.conf import settings

class Expert(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    image = models.ImageField(upload_to='expert_images/')  # Ensure MEDIA_URL and MEDIA_ROOT are configured

    def __str__(self):
        return self.name
