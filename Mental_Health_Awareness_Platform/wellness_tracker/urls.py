from django.urls import path
from . import views

urlpatterns = [
    path('reflection/', views.add_reflection, name='add_reflection'),
    path('reflections/', views.reflection_list, name='reflection_list'),
]
