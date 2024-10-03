from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserProfileForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/Profile.html', {'form': form})