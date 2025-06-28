from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reflection, WellnessGoal, WellnessActivity, WellnessReminder

class ReflectionForm(forms.ModelForm):
    """Enhanced form for daily reflections"""
    
    class Meta:
        model = Reflection
        fields = [
            'mood_rating', 'anxiety_level', 'stress_level',
            'sleep_hours', 'sleep_quality', 'exercise_minutes',
            'water_intake_glasses', 'social_interactions',
            'reflection_text', 'gratitude_entries', 'challenges_faced',
            'coping_strategies', 'daily_goals', 'goals_achieved',
            'support_received', 'support_provided', 'medication_taken',
            'therapy_session', 'self_care_activities'
        ]
        widgets = {
            'mood_rating': forms.Select(attrs={
                'class': 'form-select',
                'id': 'mood-rating'
            }),
            'anxiety_level': forms.Select(attrs={
                'class': 'form-select',
                'id': 'anxiety-level'
            }),
            'stress_level': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'max': '10',
                'type': 'range',
                'id': 'stress-level'
            }),
            'sleep_hours': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '24',
                'step': '0.5',
                'placeholder': 'e.g., 7.5'
            }),
            'sleep_quality': forms.Select(attrs={
                'class': 'form-select'
            }),
            'exercise_minutes': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '480',
                'placeholder': 'Minutes of exercise'
            }),
            'water_intake_glasses': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '20',
                'placeholder': 'Number of glasses'
            }),
            'social_interactions': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '50',
                'placeholder': 'Number of interactions'
            }),
            'reflection_text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '4',
                'placeholder': 'How are you feeling today? What\'s on your mind?'
            }),
            'gratitude_entries': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'What are you grateful for today? (one per line)'
            }),
            'challenges_faced': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'What challenges did you face today?'
            }),
            'coping_strategies': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'How did you cope with challenges?'
            }),
            'daily_goals': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'What are your goals for today? (one per line)'
            }),
            'goals_achieved': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'What goals did you achieve today? (one per line)'
            }),
            'self_care_activities': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'What self-care activities did you do? (one per line)'
            })
        }

    def clean_sleep_hours(self):
        """Validate sleep hours"""
        sleep_hours = self.cleaned_data.get('sleep_hours')
        if sleep_hours is not None:
            if sleep_hours < 0 or sleep_hours > 24:
                raise ValidationError('Sleep hours must be between 0 and 24.')
        return sleep_hours

    def clean_exercise_minutes(self):
        """Validate exercise minutes"""
        exercise_minutes = self.cleaned_data.get('exercise_minutes')
        if exercise_minutes is not None and exercise_minutes < 0:
            raise ValidationError('Exercise minutes cannot be negative.')
        return exercise_minutes

    def clean_gratitude_entries(self):
        """Convert gratitude text to list"""
        gratitude_text = self.cleaned_data.get('gratitude_entries', '')
        if gratitude_text:
            entries = [entry.strip() for entry in gratitude_text.split('\n') if entry.strip()]
            return entries
        return []

    def clean_daily_goals(self):
        """Convert daily goals text to list"""
        goals_text = self.cleaned_data.get('daily_goals', '')
        if goals_text:
            goals = [goal.strip() for goal in goals_text.split('\n') if goal.strip()]
            return goals
        return []

    def clean_goals_achieved(self):
        """Convert achieved goals text to list"""
        achieved_text = self.cleaned_data.get('goals_achieved', '')
        if achieved_text:
            achieved = [goal.strip() for goal in achieved_text.split('\n') if goal.strip()]
            return achieved
        return []

    def clean_self_care_activities(self):
        """Convert self-care activities text to list"""
        activities_text = self.cleaned_data.get('self_care_activities', '')
        if activities_text:
            activities = [activity.strip() for activity in activities_text.split('\n') if activity.strip()]
            return activities
        return []

class WellnessGoalForm(forms.ModelForm):
    """Enhanced form for wellness goals"""
    
    class Meta:
        model = WellnessGoal
        fields = [
            'title', 'description', 'goal_type', 'frequency',
            'target_value', 'unit', 'start_date', 'target_date',
            'priority', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Daily Meditation'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'Describe your goal and why it\'s important to you'
            }),
            'goal_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'target_value': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'step': '0.01',
                'placeholder': 'e.g., 30'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., minutes, glasses, times'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'target_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

    def clean_target_date(self):
        """Validate target date"""
        target_date = self.cleaned_data.get('target_date')
        start_date = self.cleaned_data.get('start_date')
        
        if target_date and start_date and target_date <= start_date:
            raise ValidationError('Target date must be after start date.')
        
        return target_date

    def clean_target_value(self):
        """Validate target value"""
        target_value = self.cleaned_data.get('target_value')
        if target_value is not None and target_value <= 0:
            raise ValidationError('Target value must be greater than 0.')
        return target_value

class WellnessActivityForm(forms.ModelForm):
    """Enhanced form for wellness activities"""
    
    class Meta:
        model = WellnessActivity
        fields = [
            'activity_type', 'title', 'description', 'duration_minutes',
            'mood_before', 'mood_after', 'energy_level', 'completed',
            'scheduled_date'
        ]
        widgets = {
            'activity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Morning Meditation'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'Describe the activity and any notes'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '480',
                'placeholder': 'Duration in minutes'
            }),
            'mood_before': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mood_after': forms.Select(attrs={
                'class': 'form-select'
            }),
            'energy_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            })
        }

    def clean_duration_minutes(self):
        """Validate duration minutes"""
        duration = self.cleaned_data.get('duration_minutes')
        if duration is not None and duration < 0:
            raise ValidationError('Duration cannot be negative.')
        return duration

    def clean_scheduled_date(self):
        """Validate scheduled date"""
        scheduled_date = self.cleaned_data.get('scheduled_date')
        if scheduled_date and scheduled_date < timezone.now():
            raise ValidationError('Scheduled date cannot be in the past.')
        return scheduled_date

class WellnessReminderForm(forms.ModelForm):
    """Enhanced form for wellness reminders"""
    
    class Meta:
        model = WellnessReminder
        fields = [
            'title', 'reminder_type', 'description', 'time',
            'days_of_week', 'is_active', 'notification_method'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Morning Meditation'
            }),
            'reminder_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': '3',
                'placeholder': 'Description of the reminder'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'days_of_week': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox-group'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'notification_method': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def clean_days_of_week(self):
        """Validate days of week selection"""
        days = self.cleaned_data.get('days_of_week')
        if not days:
            raise ValidationError('Please select at least one day of the week.')
        return days

class QuickReflectionForm(forms.Form):
    """Quick reflection form for rapid mood tracking"""
    
    MOOD_CHOICES = [
        (1, '😢 Very Sad'),
        (2, '😔 Sad'),
        (3, '😐 Neutral'),
        (4, '😊 Happy'),
        (5, '😄 Very Happy'),
    ]
    
    mood_rating = forms.ChoiceField(
        choices=MOOD_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'mood-radio-group'
        }),
        label='How are you feeling?'
    )
    
    quick_note = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': '2',
            'placeholder': 'Quick note (optional)'
        }),
        required=False,
        label='Quick Note'
    )

class GoalProgressForm(forms.Form):
    """Form for updating goal progress"""
    
    progress_value = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': '0',
            'step': '0.01'
        }),
        label='Progress Value'
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': '2',
            'placeholder': 'Any notes about your progress'
        }),
        required=False,
        label='Notes'
    )

class ActivityLogForm(forms.Form):
    """Form for logging quick activities"""
    
    ACTIVITY_CHOICES = [
        ('meditation', '🧘‍♀️ Meditation'),
        ('exercise', '🏃‍♀️ Exercise'),
        ('reading', '📚 Reading'),
        ('journaling', '📝 Journaling'),
        ('social', '👥 Social Activity'),
        ('hobby', '🎨 Hobby'),
        ('self_care', '💆‍♀️ Self Care'),
        ('custom', '✨ Custom Activity'),
    ]
    
    activity_type = forms.ChoiceField(
        choices=ACTIVITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Activity Type'
    )
    
    duration_minutes = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': '1',
            'max': '480',
            'placeholder': 'Duration in minutes'
        }),
        label='Duration (minutes)',
        required=False
    )
    
    mood_impact = forms.ChoiceField(
        choices=[
            ('positive', '😊 Positive'),
            ('neutral', '😐 Neutral'),
            ('negative', '😔 Negative'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'mood-impact-radio'
        }),
        label='How did this activity affect your mood?',
        required=False
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': '2',
            'placeholder': 'Any notes about the activity'
        }),
        required=False,
        label='Notes'
    ) 