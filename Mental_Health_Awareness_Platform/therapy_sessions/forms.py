from django import forms
from django.contrib.auth import get_user_model
from .models import TherapySession

User = get_user_model()

class ScheduleSessionForm(forms.ModelForm):
    class Meta:
        model = TherapySession
        fields = ['therapist', 'session_date', 'session_duration']
        widgets = {
            'session_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        # Check if the user is in the kwargs
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super(ScheduleSessionForm, self).__init__(*args, **kwargs)
        
        # Filter the therapist field to only include users with the therapist role
        if user:
            self.fields['therapist'].queryset = User.objects.filter(role='therapist')
        else:
            self.fields['therapist'].queryset = User.objects.none()  # No users if no user is provided
