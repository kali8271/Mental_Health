from django.urls import path
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='admin_dashboard'),  # Admin dashboard URL
]
