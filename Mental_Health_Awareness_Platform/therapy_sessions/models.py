from django.db import models
from django.conf import settings
from django.utils import timezone

class TherapySession(models.Model):
    therapist = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='therapist_sessions'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name='client_sessions', 
        null=True, 
        blank=True  # Allow NULL and blank values
    )
    session_date = models.DateTimeField()
    session_duration = models.IntegerField(help_text="Duration in minutes")
    booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.client:
            return f"Session with {self.client.username} on {self.session_date}"
        return f"Available session with {self.therapist.username} on {self.session_date}"

    def calculate_price(self):
        rate_per_minute = 10.00  # Set your desired rate per minute
        return self.session_duration * rate_per_minute

    class Meta:
        ordering = ['-session_date']  # Order sessions by date, newest first
