from django.db import models
from django.conf import settings
from django.utils import timezone

class Reflection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    mood = models.CharField(max_length=50)
    thoughts = models.TextField()
    gratitude = models.TextField()

    class Meta:
        unique_together = ('user', 'date')  # Ensure one reflection per user per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s reflection on {self.date}"
