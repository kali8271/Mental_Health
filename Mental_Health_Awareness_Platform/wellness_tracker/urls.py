from django.urls import path
from . import views

app_name = 'wellness_tracker'

urlpatterns = [
    path('', views.reflection_list, name='reflection_list'),
    path('reflection/', views.reflection, name='reflection'),
    path('reflections/', views.reflection_list, name='reflection_list'),
    path('goals/', views.goals_list, name='goals_list'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('activities/', views.activities_list, name='activities_list'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/mood-data/', views.api_mood_data, name='api_mood_data'),
    path('api/activity-data/', views.api_activity_data, name='api_activity_data'),
]
