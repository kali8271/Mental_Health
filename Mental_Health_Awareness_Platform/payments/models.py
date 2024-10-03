from django.db import models
from django.conf import settings
from therapy_sessions.models import TherapySession  # Correctly reference TherapySession

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(TherapySession, on_delete=models.CASCADE)  # Use TherapySession here
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} for session {self.session.id}"
