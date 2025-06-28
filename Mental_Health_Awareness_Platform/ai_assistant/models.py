from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import json

User = get_user_model()

class Conversation(models.Model):
    """Track AI conversation sessions with users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Conversation context
    context = models.JSONField(default=dict)  # Store conversation context
    mood_trend = models.JSONField(default=list)  # Track mood changes during conversation
    topics_discussed = models.JSONField(default=list)  # Topics covered in conversation
    
    # Crisis detection
    crisis_detected = models.BooleanField(default=False)
    crisis_level = models.IntegerField(
        choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')],
        default=1
    )
    crisis_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'AI Conversation'
        verbose_name_plural = 'AI Conversations'
    
    def __str__(self):
        return f"{self.user.username} - {self.session_id} ({self.started_at.date()})"
    
    @property
    def duration_minutes(self):
        """Calculate conversation duration in minutes"""
        if self.ended_at:
            return int((self.ended_at - self.started_at).total_seconds() / 60)
        return int((timezone.now() - self.started_at).total_seconds() / 60)
    
    def end_conversation(self):
        """End the conversation session"""
        self.ended_at = timezone.now()
        self.is_active = False
        self.save()

class Message(models.Model):
    """Individual messages in AI conversations"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('ai', 'AI Response'),
        ('system', 'System Message'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    
    # Sentiment analysis
    sentiment_score = models.FloatField(null=True, blank=True)  # -1 to 1
    emotion_detected = models.CharField(max_length=50, blank=True)  # e.g., 'sad', 'anxious', 'happy'
    confidence_score = models.FloatField(null=True, blank=True)  # 0 to 1
    
    # Message metadata
    timestamp = models.DateTimeField(default=timezone.now)
    processing_time = models.FloatField(null=True, blank=True)  # Response time in seconds
    
    # AI response specific
    ai_model_used = models.CharField(max_length=50, blank=True)  # e.g., 'gpt-4', 'gpt-3.5-turbo'
    tokens_used = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'AI Message'
        verbose_name_plural = 'AI Messages'
    
    def __str__(self):
        return f"{self.conversation.session_id} - {self.message_type} ({self.timestamp})"

class MoodAnalysis(models.Model):
    """Detailed mood analysis from AI conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_mood_analyses')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='mood_analyses')
    
    # Mood metrics
    overall_mood = models.FloatField(validators=[MinValueValidator(-1), MaxValueValidator(1)])  # -1 to 1
    anxiety_level = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=True, blank=True)
    stress_level = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=True, blank=True)
    depression_indicators = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=True, blank=True)
    
    # Emotional breakdown
    emotions_detected = models.JSONField(default=dict)  # {'sad': 0.8, 'anxious': 0.6, ...}
    dominant_emotion = models.CharField(max_length=50, blank=True)
    
    # Risk assessment
    suicide_risk = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    self_harm_risk = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    crisis_indicators = models.JSONField(default=list)  # List of concerning phrases/patterns
    
    # Analysis metadata
    analyzed_at = models.DateTimeField(default=timezone.now)
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    model_version = models.CharField(max_length=50, default='v1.0')
    
    class Meta:
        ordering = ['-analyzed_at']
        verbose_name = 'AI Mood Analysis'
        verbose_name_plural = 'AI Mood Analyses'
    
    def __str__(self):
        return f"{self.user.username} - {self.analyzed_at.date()} (Mood: {self.overall_mood:.2f})"
    
    @property
    def risk_level(self):
        """Calculate overall risk level"""
        max_risk = max(self.suicide_risk, self.self_harm_risk)
        if max_risk >= 0.8:
            return 'critical'
        elif max_risk >= 0.6:
            return 'high'
        elif max_risk >= 0.4:
            return 'medium'
        else:
            return 'low'

class Recommendation(models.Model):
    """AI-generated personalized recommendations"""
    RECOMMENDATION_TYPES = [
        ('coping', 'Coping Strategy'),
        ('activity', 'Wellness Activity'),
        ('resource', 'Resource Suggestion'),
        ('professional', 'Professional Help'),
        ('self_care', 'Self Care'),
        ('crisis', 'Crisis Intervention'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_recommendations')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='recommendations', null=True, blank=True)
    
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()  # Detailed recommendation content
    
    # Recommendation metadata
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Urgent')], default=2)
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # User interaction
    is_read = models.BooleanField(default=False)
    is_followed = models.BooleanField(default=False)
    feedback_rating = models.IntegerField(choices=[(1, 'Not Helpful'), (2, 'Somewhat Helpful'), (3, 'Helpful'), (4, 'Very Helpful'), (5, 'Extremely Helpful')], null=True, blank=True)
    feedback_notes = models.TextField(blank=True)
    
    # AI generation info
    generated_at = models.DateTimeField(default=timezone.now)
    ai_model_used = models.CharField(max_length=50, blank=True)
    context_data = models.JSONField(default=dict)  # Data used to generate recommendation
    
    class Meta:
        ordering = ['-generated_at']
        verbose_name = 'AI Recommendation'
        verbose_name_plural = 'AI Recommendations'
    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.recommendation_type})"

class CrisisAlert(models.Model):
    """Crisis detection and alert system"""
    CRISIS_TYPES = [
        ('suicide', 'Suicide Risk'),
        ('self_harm', 'Self Harm'),
        ('violence', 'Violence Risk'),
        ('psychosis', 'Psychosis'),
        ('substance', 'Substance Abuse'),
        ('other', 'Other Crisis'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crisis_alerts')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='crisis_alerts', null=True, blank=True)
    
    crisis_type = models.CharField(max_length=20, choices=CRISIS_TYPES)
    severity_level = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')])
    
    # Crisis details
    description = models.TextField()
    detected_phrases = models.JSONField(default=list)  # Phrases that triggered the alert
    risk_factors = models.JSONField(default=list)  # Identified risk factors
    
    # Response tracking
    is_acknowledged = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    response_notes = models.TextField(blank=True)
    
    # Emergency contacts
    emergency_contact_notified = models.BooleanField(default=False)
    professional_help_recommended = models.BooleanField(default=False)
    
    # Timestamps
    detected_at = models.DateTimeField(default=timezone.now)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-detected_at']
        verbose_name = 'Crisis Alert'
        verbose_name_plural = 'Crisis Alerts'
    
    def __str__(self):
        return f"{self.user.username} - {self.crisis_type} ({self.severity_level}) - {self.detected_at.date()}"
    
    def acknowledge_alert(self):
        """Mark crisis alert as acknowledged"""
        self.is_acknowledged = True
        self.acknowledged_at = timezone.now()
        self.save()
    
    def resolve_alert(self, notes=""):
        """Mark crisis alert as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.response_notes = notes
        self.save()

class UserProfile(models.Model):
    """Extended user profile for AI personalization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_profile')
    
    # Personalization data
    preferred_communication_style = models.CharField(
        max_length=20,
        choices=[('direct', 'Direct'), ('empathetic', 'Empathetic'), ('professional', 'Professional'), ('casual', 'Casual')],
        default='empathetic'
    )
    
    # Mental health history (anonymized)
    has_previous_therapy = models.BooleanField(default=False)
    current_medications = models.JSONField(default=list)
    diagnosed_conditions = models.JSONField(default=list)
    triggers = models.JSONField(default=list)  # Known triggers
    coping_strategies = models.JSONField(default=list)  # Effective coping methods
    
    # AI interaction preferences
    ai_interaction_frequency = models.CharField(
        max_length=20,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('as_needed', 'As Needed')],
        default='as_needed'
    )
    
    # Privacy settings
    allow_mood_tracking = models.BooleanField(default=True)
    allow_crisis_detection = models.BooleanField(default=True)
    allow_personalized_recommendations = models.BooleanField(default=True)
    
    # Emergency contacts
    emergency_contacts = models.JSONField(default=list)  # List of emergency contact info
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'AI User Profile'
        verbose_name_plural = 'AI User Profiles'
    
    def __str__(self):
        return f"AI Profile - {self.user.username}"
