from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import UserProfileForm, UserRegistrationForm, TherapistProfileForm, ClientProfileForm
from .models import UserProfile, TherapistProfile, ClientProfile, Notification
import json

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role', 'client')
            user.save()
            
            # Create appropriate profile based on role
            if user.role == 'therapist':
                TherapistProfile.objects.create(user=user)
            elif user.role == 'client':
                ClientProfile.objects.create(user=user)
            
            # Log in the user
            login(request, user)
            messages.success(request, f'Welcome to our platform, {user.first_name or user.username}!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        # Handle different profile types
        if user.role == 'therapist':
            form = TherapistProfileForm(request.POST, request.FILES, instance=user.therapist_profile)
        elif user.role == 'client':
            form = ClientProfileForm(request.POST, request.FILES, instance=user.client_profile)
        else:
            form = UserProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        # Prepopulate form with existing data
        if user.role == 'therapist':
            form = TherapistProfileForm(instance=user.therapist_profile)
        elif user.role == 'client':
            form = ClientProfileForm(instance=user.client_profile)
        else:
            form = UserProfileForm(instance=user)

    # Get user's recent activity
    recent_reflections = user.reflections.all()[:5] if hasattr(user, 'reflections') else []
    recent_sessions = user.session_set.all()[:5] if hasattr(user, 'session_set') else []
    
    context = {
        'form': form,
        'user_profile': user,
        'recent_reflections': recent_reflections,
        'recent_sessions': recent_sessions,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    """Enhanced dashboard with user statistics and recent activity"""
    user = request.user
    
    # Get user statistics
    stats = {
        'total_reflections': user.reflections.count() if hasattr(user, 'reflections') else 0,
        'total_sessions': user.session_set.count() if hasattr(user, 'session_set') else 0,
        'current_streak': 0,  # Calculate from wellness tracker
        'wellness_score': 0,  # Calculate average wellness score
    }
    
    # Get recent activity
    recent_reflections = user.reflections.all()[:3] if hasattr(user, 'reflections') else []
    upcoming_sessions = user.session_set.filter(date__gte=timezone.now().date())[:3] if hasattr(user, 'session_set') else []
    
    # Get notifications
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]
    
    context = {
        'stats': stats,
        'recent_reflections': recent_reflections,
        'upcoming_sessions': upcoming_sessions,
        'notifications': notifications,
    }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
@require_POST
def update_notification_preferences(request):
    """Update user notification preferences"""
    try:
        data = json.loads(request.body)
        user = request.user
        user.notification_preferences.update(data.get('preferences', {}))
        user.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        auth_logout(request)
        messages.success(request, 'Your account has been deactivated successfully.')
        return redirect('home')
    
    return render(request, 'accounts/delete_account.html')

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        # Handle password change logic
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('login')
    
    return render(request, 'accounts/change_password.html')

@login_required
def privacy_settings(request):
    """Manage privacy settings"""
    user = request.user
    
    if request.method == 'POST':
        # Update privacy settings
        user.profile_visibility = request.POST.get('profile_visibility', 'public')
        user.data_sharing_preferences = request.POST.get('data_sharing', 'minimal')
        user.save()
        messages.success(request, 'Privacy settings updated successfully!')
        return redirect('privacy_settings')
    
    context = {
        'user': user,
    }
    
    return render(request, 'accounts/privacy_settings.html', context)