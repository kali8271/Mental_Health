# community/urls.py

from django.urls import path
from .views import forum, create_post

app_name = 'community'

urlpatterns = [
    path('forum/', forum, name='forum'),
    path('forum/create/', create_post, name='create_post'),
]
