from django.urls import path
from . import views

app_name = 'therapy_sessions'

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('schedule/', views.schedule_session, name='schedule'),
    path('sessions/', views.session_list, name='session_list'),
    path('cancel_booking/<int:session_id>/', views.cancel_booking, name='cancel_booking'),
]

