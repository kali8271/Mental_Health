from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_session, name='schedule_session'),
    path('sessions/', views.session_list, name='session_list'),
]
