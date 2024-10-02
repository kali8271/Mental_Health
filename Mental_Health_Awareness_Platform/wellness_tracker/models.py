from django.db import models
from django.conf import settings

class WellnessEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)
    reflection = models.TextField()
    date = models.DateField(auto_now_add=True)
