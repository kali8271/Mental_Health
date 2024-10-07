# experts/views.py

from django.shortcuts import render
from .models import Expert

def expert_list(request):
    experts = Expert.objects.all()  # Fetch all experts
    return render(request, 'experts/expert_list.html', {'experts': experts})  # Ensure the template path is correct
