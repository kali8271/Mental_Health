from django import forms
from .models import Reflection

class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['mood', 'thoughts', 'gratitude']
