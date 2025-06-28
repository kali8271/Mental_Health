from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import UserProfile, TherapistProfile, ClientProfile

class UserRegistrationForm(UserCreationForm):
    """Enhanced registration form with role selection and additional fields"""
    
    # Role selection
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial='client',
        help_text='Select your role on the platform'
    )
    
    # Additional fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (Optional)'})
    )
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='Your date of birth (optional)'
    )
    
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Your gender (optional)'
    )
    
    # Password fields with enhanced styling
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text='Your password must contain at least 8 characters.'
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text='Enter the same password as before, for verification.'
    )
    
    # Terms and conditions
    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='I agree to the Terms of Service and Privacy Policy'
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'username', 'first_name', 'last_name', 'email', 'role',
            'phone_number', 'date_of_birth', 'gender', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

class UserProfileForm(forms.ModelForm):
    """Form for updating basic user profile information"""
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'bio', 'profile_picture',
            'city', 'state', 'country', 'user_timezone'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'user_timezone': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('UTC', 'UTC'),
                ('America/New_York', 'Eastern Time'),
                ('America/Chicago', 'Central Time'),
                ('America/Denver', 'Mountain Time'),
                ('America/Los_Angeles', 'Pacific Time'),
                ('Europe/London', 'London'),
                ('Europe/Paris', 'Paris'),
                ('Asia/Tokyo', 'Tokyo'),
                ('Asia/Shanghai', 'Shanghai'),
                ('Australia/Sydney', 'Sydney'),
            ]),
        }

class TherapistProfileForm(forms.ModelForm):
    """Form for therapist-specific profile information"""
    
    class Meta:
        model = TherapistProfile
        fields = [
            'license_number', 'specialization', 'years_of_experience',
            'education', 'certifications', 'therapist_photo', 'license_photo',
            'hourly_rate', 'availability_schedule', 'max_clients',
            'languages_spoken', 'treatment_approaches', 'client_populations'
        ]
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter certifications, one per line'}),
            'therapist_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'license_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'availability_schedule': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your availability schedule'}),
            'max_clients': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'languages_spoken': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter languages, separated by commas'}),
            'treatment_approaches': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter treatment approaches, one per line'}),
            'client_populations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter client populations you work with, separated by commas'}),
        }
    
    def clean_hourly_rate(self):
        rate = self.cleaned_data.get('hourly_rate')
        if rate and rate <= 0:
            raise forms.ValidationError('Hourly rate must be greater than zero.')
        return rate
    
    def clean_license_number(self):
        license_num = self.cleaned_data.get('license_number')
        if TherapistProfile.objects.filter(license_number=license_num).exclude(user=self.instance.user).exists():
            raise forms.ValidationError('This license number is already registered.')
        return license_num

class ClientProfileForm(forms.ModelForm):
    """Form for client-specific profile information"""
    
    class Meta:
        model = ClientProfile
        fields = [
            'client_photo', 'emergency_contact_name', 'emergency_contact_relationship',
            'medical_history', 'current_medications', 'allergies',
            'preferred_therapy_type', 'preferred_gender', 'session_duration_preference',
            'therapy_goals'
        ]
        widgets = {
            'client_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter current medications, one per line'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter allergies, separated by commas'}),
            'preferred_therapy_type': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select preferred therapy type'),
                ('cbt', 'Cognitive Behavioral Therapy (CBT)'),
                ('dbt', 'Dialectical Behavior Therapy (DBT)'),
                ('psychodynamic', 'Psychodynamic Therapy'),
                ('humanistic', 'Humanistic Therapy'),
                ('family', 'Family Therapy'),
                ('group', 'Group Therapy'),
                ('other', 'Other'),
            ]),
            'preferred_gender': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'No preference'),
                ('male', 'Male'),
                ('female', 'Female'),
                ('non_binary', 'Non-binary'),
            ]),
            'session_duration_preference': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('30min', '30 minutes'),
                ('45min', '45 minutes'),
                ('60min', '60 minutes'),
                ('90min', '90 minutes'),
            ]),
            'therapy_goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your therapy goals and what you hope to achieve'}),
        }

class PasswordChangeForm(forms.Form):
    """Form for changing user password"""
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
        label='Current Password'
    )
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password',
        help_text='Password must be at least 8 characters long.'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label='Confirm New Password'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('New passwords do not match.')
        
        if new_password and len(new_password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        return cleaned_data

class NotificationPreferencesForm(forms.Form):
    """Form for managing notification preferences"""
    
    email_notifications = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Email Notifications'
    )
    
    push_notifications = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Push Notifications'
    )
    
    session_reminders = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Session Reminders'
    )
    
    wellness_reminders = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Wellness Tracking Reminders'
    )
    
    community_updates = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Community Updates'
    )
    
    marketing_emails = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Marketing Emails'
    )