# admin/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin/dashboard.html')  # Admin dashboard
    else:
        return render(request, 'admin/user_dashboard.html')  # User dashboard
