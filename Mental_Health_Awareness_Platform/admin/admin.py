from django.contrib import admin
from accounts.models import UserProfile  # Example model
from therapy_sessions.models import TherapySession  # Example model

admin.site.register(UserProfile)  # Register UserProfile model
admin.site.register(TherapySession)  # Register Session model
