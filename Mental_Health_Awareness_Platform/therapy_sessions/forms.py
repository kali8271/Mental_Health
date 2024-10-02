from django import forms
from .models import TherapySession

class ScheduleSessionForm(forms.ModelForm):
    class Meta:
        model = TherapySession
        fields = ['therapist', 'session_date', 'session_duration']
        widgets = {
            'session_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
