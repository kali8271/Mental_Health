# admin/urls.py

from django.urls import path
from .views import dashboard

urlpatterns = [
    path('admin/dashboard/', dashboard, name='dashboard'),  # Unified dashboard URL
]
