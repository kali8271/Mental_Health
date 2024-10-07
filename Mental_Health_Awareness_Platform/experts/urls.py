# therapy_sessions/urls.py

from django.urls import path
from .views import expert_list  # Import the view

urlpatterns = [
    path('experts/', expert_list, name='expert_list'),  # URL to access the experts list
    # Other URL patterns...
]
