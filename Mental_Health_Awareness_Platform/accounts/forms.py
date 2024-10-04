from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role', 'bio', 'password1', 'password2']




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'bio', 'role', 'profile_picture']  # Include fields you want in the form
