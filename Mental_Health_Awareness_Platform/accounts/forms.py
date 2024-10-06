from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role', 'bio', 'client_photo', 'therapist_photo', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(choices=UserProfile.ROLES)
        self.fields['bio'].widget = forms.Textarea(attrs={'placeholder': 'Tell us about yourself...', 'rows': 4})

        # Initialize photo fields
        self.fields['client_photo'].required = False
        self.fields['therapist_photo'].required = False

        if 'role' in self.data:
            try:
                role = self.data.get('role')
                if role == 'client':
                    self.fields['therapist_photo'].widget.attrs['style'] = 'display:none;'
                elif role == 'therapist':
                    self.fields['client_photo'].widget.attrs['style'] = 'display:none;'
            except (ValueError, TypeError):
                pass  # Do not throw an error if there is an issue with the data

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        client_photo = cleaned_data.get('client_photo')
        therapist_photo = cleaned_data.get('therapist_photo')

        if role == 'client' and not client_photo:
            self.add_error('client_photo', 'Client photo is required for clients.')
        elif role == 'therapist' and not therapist_photo:
            self.add_error('therapist_photo', 'Therapist photo is required for therapists.')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'bio', 'role', 'client_photo', 'therapist_photo']  # Include relevant fields