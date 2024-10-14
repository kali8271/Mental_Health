from django.db import models
from accounts.models import UserProfile

class Expert(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    therapist = models.OneToOneField(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='expert_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # If an expert image is not provided, use the therapist's photo
        if self.therapist and not self.image:
            self.image = self.therapist.therapist_photo
        super(Expert, self).save(*args, **kwargs)

    def __str__(self):
        return self.name