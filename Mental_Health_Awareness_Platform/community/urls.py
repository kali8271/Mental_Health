# community/urls.py
from django.urls import path
from .views import ForumView

urlpatterns = [
    path('forum/', ForumView.as_view(), name='forum'),  # Add your forum view here
]
