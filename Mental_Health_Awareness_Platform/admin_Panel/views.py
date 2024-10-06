from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from .models import Professional

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(username=request.user.username)  # Get the user's profile
    professional = Professional.objects.all()
    if request.user.is_superuser:
        return render(request, 'admin/dashboard.html', {'user_profile': user_profile,'professional ' : professional})  # Admin dashboard
    else:
        return render(request, 'admin/user_dashboard.html', {'user_profile': user_profile, 'professional' : professional})  # User dashboard
