from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserProfileForm, UserRegistrationForm
from .models import UserProfile  # Ensure UserProfile is imported
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)  # Handling file uploads
        if form.is_valid():
            user = form.save(commit=False)  # Create user but don't save to the database yet
            
            # Set the role from the form's cleaned data (if applicable)
            user.role = form.cleaned_data.get('role', 'default_role')  # Set default if role isn't provided
            user.save()  # Now save the user to the database
            
            # Automatically log in the user after registration
            login(request, user)
            return redirect('profile')  # Redirect to the user's profile page after registration
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required  # Ensure the user is logged in to access the profile page
def profile(request):
    try:
        # Get the current user's profile based on the logged-in user
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle case where the profile does not exist (optional)
        return redirect('register')  # Redirect if profile doesn't exist (adjust as needed)

    if request.method == 'POST':
        # Update the profile, including file handling for profile picture uploads
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()  # Save the updated profile data
            return redirect('profile')  # Redirect after successful update
    else:
        # Prepopulate the form with existing profile data
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/profile.html', {'form': form, 'user_profile': user_profile})
