import openai
import json
import re
from typing import Dict, List, Tuple, Optional
from django.conf import settings
from django.utils import timezone
from .models import Conversation, Message, MoodAnalysis, Recommendation, CrisisAlert, UserProfile
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Main AI service for mental health assistance"""
    
    def __init__(self):
        # Initialize OpenAI client (you'll need to set OPENAI_API_KEY in settings)
        self.client = openai.OpenAI(api_key=getattr(settings, 'OPENAI_API_KEY', ''))
        self.model = "gpt-3.5-turbo"  # Can be upgraded to gpt-4 for better performance
        
        # Crisis detection patterns
        self.crisis_patterns = {
            'suicide': [
                r'\b(kill myself|end my life|want to die|suicide|take my life)\b',
                r'\b(no reason to live|better off dead|everyone would be better)\b',
                r'\b(planning to|thinking about|going to) (kill|end|die)\b'
            ],
            'self_harm': [
                r'\b(cut myself|hurt myself|self harm|self injury)\b',
                r'\b(pain makes me feel|physical pain|bleeding)\b'
            ],
            'violence': [
                r'\b(hurt someone|kill someone|violent|attack)\b',
                r'\b(angry enough to|want to hurt|revenge)\b'
            ]
        }
        
        # Mental health knowledge base
        self.knowledge_base = {
            'coping_strategies': [
                'Deep breathing exercises',
                'Progressive muscle relaxation',
                'Mindfulness meditation',
                'Physical exercise',
                'Journaling',
                'Talking to a trusted friend',
                'Engaging in hobbies',
                'Getting adequate sleep',
                'Maintaining a routine',
                'Seeking professional help'
            ],
            'crisis_resources': {
                'suicide_prevention': '988 Suicide & Crisis Lifeline',
                'crisis_text': 'Text HOME to 741741',
                'emergency': '911 for immediate emergency',
                'mental_health_america': '1-800-273-8255'
            }
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment and emotions in text"""
        try:
            prompt = f"""
            Analyze the following text for sentiment and emotions. Return a JSON response with:
            - sentiment_score: float between -1 (very negative) and 1 (very positive)
            - emotions: list of detected emotions (e.g., ['sad', 'anxious', 'hopeful'])
            - dominant_emotion: the strongest emotion detected
            - confidence: float between 0 and 1
            
            Text: "{text}"
            
            Focus on mental health context and be sensitive to crisis indicators.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            # Fallback to basic analysis
            return {
                'sentiment_score': 0.0,
                'emotions': ['neutral'],
                'dominant_emotion': 'neutral',
                'confidence': 0.5
            }
    
    def detect_crisis(self, text: str) -> Dict:
        """Detect crisis indicators in text"""
        crisis_detected = False
        crisis_type = None
        severity = 1
        detected_phrases = []
        
        # Check for crisis patterns
        for crisis_type_name, patterns in self.crisis_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                if matches:
                    crisis_detected = True
                    crisis_type = crisis_type_name
                    detected_phrases.extend(matches)
                    
                    # Determine severity based on context
                    if any(word in text.lower() for word in ['planning', 'going to', 'will', 'definitely']):
                        severity = 4  # Critical
                    elif any(word in text.lower() for word in ['thinking about', 'considering', 'maybe']):
                        severity = 3  # High
                    else:
                        severity = 2  # Medium
        
        return {
            'crisis_detected': crisis_detected,
            'crisis_type': crisis_type,
            'severity': severity,
            'detected_phrases': detected_phrases
        }
    
    def generate_response(self, user_message: str, conversation_context: List[Dict], user_profile: UserProfile = None) -> str:
        """Generate AI response based on user message and context"""
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt(user_profile)
            
            # Build conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation context
            for msg in conversation_context[-10:]:  # Last 10 messages for context
                role = "user" if msg['type'] == 'user' else "assistant"
                messages.append({"role": role, "content": msg['content']})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return self._get_fallback_response(user_message)
    
    def generate_recommendations(self, user: User, conversation: Conversation = None) -> List[Dict]:
        """Generate personalized recommendations based on user data"""
        try:
            # Get user's recent mood data
            recent_mood = self._get_recent_mood_data(user)
            
            # Build recommendation prompt
            prompt = f"""
            Generate 3 personalized mental health recommendations for a user with the following profile:
            
            Recent mood trend: {recent_mood.get('trend', 'stable')}
            Current stress level: {recent_mood.get('stress', 'moderate')}
            Previous therapy: {getattr(user.ai_profile, 'has_previous_therapy', False)}
            
            Provide recommendations in this JSON format:
            {{
                "recommendations": [
                    {{
                        "type": "coping|activity|resource|professional|self_care",
                        "title": "Short title",
                        "description": "Brief description",
                        "content": "Detailed explanation",
                        "priority": 1-4,
                        "confidence": 0.0-1.0
                    }}
                ]
            }}
            
            Focus on evidence-based, practical suggestions that are appropriate for the user's situation.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=800
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('recommendations', [])
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return self._get_default_recommendations()
    
    def _build_system_prompt(self, user_profile: UserProfile = None) -> str:
        """Build system prompt for AI assistant"""
        base_prompt = """
        You are a compassionate, professional mental health AI assistant. Your role is to:
        
        1. Provide empathetic, supportive responses
        2. Offer evidence-based mental health information
        3. Suggest coping strategies and self-care techniques
        4. Recognize crisis situations and provide appropriate resources
        5. Encourage professional help when needed
        
        IMPORTANT GUIDELINES:
        - Always prioritize user safety
        - Never give medical advice or diagnose conditions
        - Encourage professional help for serious concerns
        - Be supportive but not overly clinical
        - Use a warm, understanding tone
        - Provide practical, actionable suggestions
        
        CRISIS RESPONSE:
        If you detect crisis indicators, immediately provide crisis resources and encourage professional help.
        """
        
        if user_profile:
            base_prompt += f"""
            
            USER PREFERENCES:
            - Communication style: {user_profile.preferred_communication_style}
            - Previous therapy: {'Yes' if user_profile.has_previous_therapy else 'No'}
            - Known triggers: {', '.join(user_profile.triggers) if user_profile.triggers else 'None specified'}
            - Effective coping strategies: {', '.join(user_profile.coping_strategies) if user_profile.coping_strategies else 'None specified'}
            """
        
        return base_prompt
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Get fallback response when AI service is unavailable"""
        if any(word in user_message.lower() for word in ['crisis', 'emergency', 'suicide', 'kill']):
            return """
            I'm here to listen and support you. If you're experiencing a crisis, please know that help is available:
            
            🚨 Crisis Resources:
            • National Suicide Prevention Lifeline: 988
            • Crisis Text Line: Text HOME to 741741
            • Emergency Services: 911
            
            You don't have to go through this alone. Professional help is available 24/7.
            """
        
        return """
        I'm here to support you. While I'm experiencing some technical difficulties, please know that:
        
        • Your feelings are valid and important
        • Professional help is available if you need it
        • You're not alone in this journey
        
        Would you like to try again in a moment, or would you prefer to speak with a human counselor?
        """
    
    def _get_recent_mood_data(self, user: User) -> Dict:
        """Get user's recent mood data for personalization"""
        try:
            # Get recent mood analyses
            recent_analyses = MoodAnalysis.objects.filter(user=user).order_by('-analyzed_at')[:7]
            
            if not recent_analyses:
                return {'trend': 'stable', 'stress': 'moderate'}
            
            # Calculate trend
            moods = [analysis.overall_mood for analysis in recent_analyses]
            avg_mood = sum(moods) / len(moods)
            
            if avg_mood > 0.3:
                trend = 'improving'
            elif avg_mood < -0.3:
                trend = 'declining'
            else:
                trend = 'stable'
            
            # Get stress level
            stress_levels = [analysis.stress_level for analysis in recent_analyses if analysis.stress_level]
            avg_stress = sum(stress_levels) / len(stress_levels) if stress_levels else 0.5
            
            if avg_stress > 0.7:
                stress = 'high'
            elif avg_stress < 0.3:
                stress = 'low'
            else:
                stress = 'moderate'
            
            return {'trend': trend, 'stress': stress}
            
        except Exception as e:
            logger.error(f"Error getting mood data: {e}")
            return {'trend': 'stable', 'stress': 'moderate'}
    
    def _get_default_recommendations(self) -> List[Dict]:
        """Get default recommendations when AI generation fails"""
        return [
            {
                'type': 'self_care',
                'title': 'Practice Self-Care',
                'description': 'Take time for activities that bring you joy and relaxation',
                'content': 'Self-care is essential for mental health. Try activities like reading, taking a warm bath, or spending time in nature.',
                'priority': 2,
                'confidence': 0.8
            },
            {
                'type': 'coping',
                'title': 'Deep Breathing Exercise',
                'description': 'A simple technique to reduce stress and anxiety',
                'content': 'Find a quiet place, sit comfortably, and take slow, deep breaths. Inhale for 4 counts, hold for 4, exhale for 4.',
                'priority': 2,
                'confidence': 0.9
            },
            {
                'type': 'professional',
                'title': 'Consider Professional Support',
                'description': 'Professional help can provide valuable tools and support',
                'content': 'If you\'re struggling, consider reaching out to a mental health professional. They can provide personalized support and evidence-based treatments.',
                'priority': 3,
                'confidence': 0.7
            }
        ]

class ConversationManager:
    """Manage AI conversation sessions"""
    
    def __init__(self, user):
        self.user = user
        self.ai_service = AIService()
    
    def start_conversation(self) -> Conversation:
        """Start a new conversation session"""
        import uuid
        
        session_id = str(uuid.uuid4())
        conversation = Conversation.objects.create(
            user=self.user,
            session_id=session_id,
            is_active=True
        )
        
        # Create welcome message
        welcome_message = self._get_welcome_message()
        Message.objects.create(
            conversation=conversation,
            message_type='ai',
            content=welcome_message,
            ai_model_used='gpt-3.5-turbo'
        )
        
        return conversation
    
    def send_message(self, conversation: Conversation, user_message: str) -> Dict:
        """Process user message and generate AI response"""
        start_time = timezone.now()
        
        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            message_type='user',
            content=user_message
        )
        
        # Analyze sentiment
        sentiment_result = self.ai_service.analyze_sentiment(user_message)
        user_msg.sentiment_score = sentiment_result.get('sentiment_score')
        user_msg.emotion_detected = sentiment_result.get('dominant_emotion')
        user_msg.confidence_score = sentiment_result.get('confidence')
        user_msg.save()
        
        # Detect crisis
        crisis_result = self.ai_service.detect_crisis(user_message)
        if crisis_result['crisis_detected']:
            self._handle_crisis_detection(conversation, crisis_result, user_message)
        
        # Get conversation context
        context = self._get_conversation_context(conversation)
        
        # Generate AI response
        ai_response = self.ai_service.generate_response(
            user_message, 
            context, 
            getattr(self.user, 'ai_profile', None)
        )
        
        # Calculate processing time
        processing_time = (timezone.now() - start_time).total_seconds()
        
        # Save AI response
        ai_msg = Message.objects.create(
            conversation=conversation,
            message_type='ai',
            content=ai_response,
            processing_time=processing_time,
            ai_model_used='gpt-3.5-turbo'
        )
        
        # Update conversation context
        conversation.context.update({
            'last_mood': sentiment_result.get('sentiment_score', 0),
            'last_emotion': sentiment_result.get('dominant_emotion', 'neutral'),
            'crisis_detected': crisis_result['crisis_detected']
        })
        conversation.save()
        
        return {
            'response': ai_response,
            'sentiment': sentiment_result,
            'crisis_detected': crisis_result['crisis_detected'],
            'processing_time': processing_time
        }
    
    def _get_welcome_message(self) -> str:
        """Get personalized welcome message"""
        return f"""
        Hello! I'm here to support you on your mental health journey. 👋

        I'm an AI assistant designed to provide compassionate support, helpful information, and evidence-based suggestions. I can help you with:

        • Understanding your emotions and mood patterns
        • Learning coping strategies and self-care techniques
        • Finding mental health resources and information
        • Providing a safe space to talk about your feelings

        Remember: I'm here to support you, but I'm not a replacement for professional mental health care. If you're experiencing a crisis, please reach out to emergency services or a crisis hotline.

        How are you feeling today? What would you like to talk about?
        """
    
    def _get_conversation_context(self, conversation: Conversation) -> List[Dict]:
        """Get conversation context for AI"""
        messages = conversation.messages.all().order_by('timestamp')
        context = []
        
        for msg in messages:
            context.append({
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            })
        
        return context
    
    def _handle_crisis_detection(self, conversation: Conversation, crisis_result: Dict, user_message: str):
        """Handle crisis detection"""
        # Create crisis alert
        CrisisAlert.objects.create(
            user=self.user,
            conversation=conversation,
            crisis_type=crisis_result['crisis_type'],
            severity_level=crisis_result['severity'],
            description=f"Crisis detected in conversation: {user_message[:100]}...",
            detected_phrases=crisis_result['detected_phrases']
        )
        
        # Update conversation
        conversation.crisis_detected = True
        conversation.crisis_level = crisis_result['severity']
        conversation.save() 