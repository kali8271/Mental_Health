from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('chat/', views.chat_interface, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('history/', views.conversation_history, name='history'),
    path('conversation/<str:session_id>/', views.view_conversation, name='view_conversation'),
] 