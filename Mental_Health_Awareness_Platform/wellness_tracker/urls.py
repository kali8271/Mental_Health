from django.urls import path
from . import views

urlpatterns = [
    path('entry/', views.wellness_entry, name='wellness_entry'),
    path('entries/', views.wellness_entries, name='wellness_entries'),
]
