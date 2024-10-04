from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserProfileForm, UserRegistrationForm
from .models import UserProfile  # Import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a UserProfile instance with the newly created user
            UserProfile.objects.create(
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role='client',  # Set a default role or use the form to choose
                password=user.password  # Ensure the password is hashed correctly
            )
            login(request, user)  # Log the user in
            return redirect('Profile')  # Redirect to the profile page
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def profile(request):
    user_profile = UserProfile.objects.get(username=request.user.username)  # Get the user's profile by username

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('Profile')  # Redirect after saving
    else:
        form = UserProfileForm(instance=user_profile)  # Load existing profile data into the form

    return render(request, 'accounts/Profile.html', {'form': form, 'user_profile': user_profile})
