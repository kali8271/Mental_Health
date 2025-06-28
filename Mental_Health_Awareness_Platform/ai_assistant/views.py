from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Conversation, Message
from .services import ConversationManager
import json

# Create your views here.

@login_required
def chat_interface(request):
    """Render the AI Assistant chat interface."""
    # Get or start a conversation
    conversation = Conversation.objects.filter(user=request.user, is_active=True).first()
    if not conversation:
        manager = ConversationManager(request.user)
        conversation = manager.start_conversation()
    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'ai_assistant/chat.html', {
        'conversation': conversation,
        'messages': messages,
    })

@login_required
@csrf_exempt  # For AJAX POSTs (ensure you use CSRF token in production)
def send_message(request):
    """Handle user message, generate AI response, and return JSON."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8')) if request.body else request.POST
        user_message = data.get('message')
        conversation_id = data.get('conversation_id')
        if not user_message or not conversation_id:
            return HttpResponseBadRequest('Missing message or conversation_id')
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        manager = ConversationManager(request.user)
        result = manager.send_message(conversation, user_message)
        return JsonResponse({
            'response': result['response'],
            'sentiment': result['sentiment'],
            'crisis_detected': result['crisis_detected'],
            'processing_time': result['processing_time'],
        })
    return HttpResponseBadRequest('Invalid request method')

@login_required
def conversation_history(request):
    """List user's past AI conversations."""
    conversations = Conversation.objects.filter(user=request.user).order_by('-started_at')
    return render(request, 'ai_assistant/history.html', {
        'conversations': conversations
    })

@login_required
def view_conversation(request, session_id):
    """View a specific conversation and its messages."""
    conversation = get_object_or_404(Conversation, session_id=session_id, user=request.user)
    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'ai_assistant/conversation.html', {
        'conversation': conversation,
        'messages': messages
    })
