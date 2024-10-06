from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import  UserProfileForm, UserRegistrationForm
from .models import UserProfile  # Import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)  # Add request.FILES to handle file uploads
        if form.is_valid():
            user = form.save()  # Save the UserProfile instance directly
            
            # Set default role if not set
            user.role = form.cleaned_data['role']  # Use selected role from the form
            user.save()  # Save the updated UserProfile instance
            
            login(request, user)  # Log the user in after registration
            return redirect('profile')  # Redirect to the user's profile page
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    user_profile = UserProfile.objects.get(username=request.user.username)  # Get the user's profile by username

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Use UserProfileForm here
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('Profile')  # Redirect after saving
    else:
        form = UserProfileForm(instance=user_profile)  # Load existing profile data into the form

    return render(request, 'accounts/Profile.html', {'form': form, 'user_profile': user_profile})