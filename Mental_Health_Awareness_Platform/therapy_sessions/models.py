from django.db import models
from django.conf import settings
from django.utils import timezone

class TherapySession(models.Model):
    therapist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='therapist_sessions')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_sessions')
    session_date = models.DateTimeField()
    session_duration = models.IntegerField(help_text="Duration in minutes")
    booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Session with {self.client.username} on {self.session_date}"

    class Meta:
        ordering = ['-session_date']
