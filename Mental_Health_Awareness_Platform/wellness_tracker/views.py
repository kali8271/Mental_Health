from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta, date
from .models import Reflection, WellnessGoal, WellnessActivity, MoodAnalytics, WellnessStreak
from .forms import ReflectionForm, WellnessGoalForm, WellnessActivityForm
import json

@login_required
def reflection_list(request):
    """Display user's reflection history with enhanced analytics"""
    reflections = Reflection.objects.filter(user=request.user)
    
    # Get analytics data
    analytics = get_user_analytics(request.user)
    
    context = {
        'reflections': reflections,
        'analytics': analytics,
        'page_title': 'Wellness Tracker'
    }
    return render(request, 'tracker/reflection_list.html', context)

@login_required
def reflection(request):
    """Create or update daily reflection with enhanced form"""
    today = timezone.now().date()
    reflection_obj, created = Reflection.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={
            'mood_rating': 3,
            'anxiety_level': 3,
            'stress_level': 5
        }
    )
    
    if request.method == 'POST':
        form = ReflectionForm(request.POST, instance=reflection_obj)
        if form.is_valid():
            reflection_obj = form.save()
            
            # Update streaks
            update_user_streaks(request.user, today)
            
            # Generate insights
            insights = generate_insights(request.user)
            
            messages.success(request, 'Reflection saved successfully!')
            return redirect('wellness_tracker:reflection_list')
    else:
        form = ReflectionForm(instance=reflection_obj)
    
    # Get user's recent data for context
    recent_data = get_recent_user_data(request.user)
    
    context = {
        'form': form,
        'reflection': reflection_obj,
        'recent_data': recent_data,
        'page_title': 'Daily Reflection'
    }
    return render(request, 'tracker/reflection.html', context)

@login_required
def goals_list(request):
    """Manage wellness goals"""
    goals = WellnessGoal.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = WellnessGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('wellness_tracker:goals_list')
    else:
        form = WellnessGoalForm()
    
    context = {
        'goals': goals,
        'form': form,
        'page_title': 'Wellness Goals'
    }
    return render(request, 'tracker/goals_list.html', context)

@login_required
def goal_detail(request, goal_id):
    """View and update specific goal"""
    goal = get_object_or_404(WellnessGoal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        form = WellnessGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully!')
            return redirect('wellness_tracker:goals_list')
    else:
        form = WellnessGoalForm(instance=goal)
    
    # Get goal progress data
    progress_data = get_goal_progress(goal)
    
    context = {
        'goal': goal,
        'form': form,
        'progress_data': progress_data,
        'page_title': f'Goal: {goal.title}'
    }
    return render(request, 'tracker/goal_detail.html', context)

@login_required
def activities_list(request):
    """Manage wellness activities"""
    activities = WellnessActivity.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = WellnessActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity created successfully!')
            return redirect('wellness_tracker:activities_list')
    else:
        form = WellnessActivityForm()
    
    context = {
        'activities': activities,
        'form': form,
        'page_title': 'Wellness Activities'
    }
    return render(request, 'tracker/activities_list.html', context)

@login_required
def analytics_dashboard(request):
    """Enhanced analytics dashboard"""
    user = request.user
    
    # Get comprehensive analytics
    analytics = get_user_analytics(user)
    streaks = get_user_streaks(user)
    insights = generate_insights(user)
    
    context = {
        'analytics': analytics,
        'streaks': streaks,
        'insights': insights,
        'page_title': 'Analytics Dashboard'
    }
    return render(request, 'tracker/analytics_dashboard.html', context)

@login_required
def api_mood_data(request):
    """API endpoint for mood chart data"""
    days = int(request.GET.get('days', 7))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    reflections = Reflection.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    data = {
        'labels': [],
        'mood': [],
        'anxiety': [],
        'stress': []
    }
    
    for reflection in reflections:
        data['labels'].append(reflection.date.strftime('%m/%d'))
        data['mood'].append(reflection.mood_rating)
        data['anxiety'].append(reflection.anxiety_level)
        data['stress'].append(reflection.stress_level)
    
    return JsonResponse(data)

@login_required
def api_activity_data(request):
    """API endpoint for activity distribution data"""
    days = int(request.GET.get('days', 7))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    reflections = Reflection.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )
    
    # Calculate activity totals
    total_exercise = sum(r.exercise_minutes for r in reflections)
    total_social = sum(r.social_interactions for r in reflections)
    total_water = sum(r.water_intake_glasses for r in reflections)
    
    # Count activities from JSON field
    total_activities = 0
    for reflection in reflections:
        total_activities += len(reflection.activities_completed)
    
    data = {
        'labels': ['Exercise', 'Social', 'Water', 'Activities'],
        'values': [total_exercise, total_social, total_water, total_activities]
    }
    
    return JsonResponse(data)

# Helper functions
def get_user_analytics(user):
    """Get comprehensive user analytics"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Recent reflections
    recent_reflections = Reflection.objects.filter(
        user=user,
        date__gte=week_ago
    ).order_by('-date')
    
    # Calculate averages
    avg_mood = recent_reflections.aggregate(Avg('mood_rating'))['mood_rating__avg'] or 0
    avg_anxiety = recent_reflections.aggregate(Avg('anxiety_level'))['anxiety_level__avg'] or 0
    avg_stress = recent_reflections.aggregate(Avg('stress_level'))['stress_level__avg'] or 0
    
    # Activity totals
    total_exercise = sum(r.exercise_minutes for r in recent_reflections)
    total_social = sum(r.social_interactions for r in recent_reflections)
    total_water = sum(r.water_intake_glasses for r in recent_reflections)
    
    # Goals progress
    active_goals = WellnessGoal.objects.filter(user=user, status='active')
    completed_goals = WellnessGoal.objects.filter(user=user, status='completed')
    
    return {
        'avg_mood': round(avg_mood, 1),
        'avg_anxiety': round(avg_anxiety, 1),
        'avg_stress': round(avg_stress, 1),
        'total_exercise': total_exercise,
        'total_social': total_social,
        'total_water': total_water,
        'active_goals': active_goals.count(),
        'completed_goals': completed_goals.count(),
        'recent_reflections': recent_reflections[:5]
    }

def get_user_streaks(user):
    """Get user's current streaks"""
    streaks = WellnessStreak.objects.filter(user=user)
    streak_data = {}
    
    for streak in streaks:
        streak_data[streak.streak_type] = {
            'current': streak.current_streak,
            'longest': streak.longest_streak
        }
    
    return streak_data

def update_user_streaks(user, activity_date):
    """Update user streaks based on activity"""
    # Update reflection streak
    streak, created = WellnessStreak.objects.get_or_create(
        user=user,
        streak_type='reflection',
        defaults={'current_streak': 0, 'longest_streak': 0}
    )
    streak.update_streak(activity_date)
    
    # Update other streaks based on reflection data
    try:
        reflection = Reflection.objects.get(user=user, date=activity_date)
        
        # Exercise streak
        if reflection.exercise_minutes > 0:
            exercise_streak, _ = WellnessStreak.objects.get_or_create(
                user=user,
                streak_type='exercise',
                defaults={'current_streak': 0, 'longest_streak': 0}
            )
            exercise_streak.update_streak(activity_date)
        
        # Water streak
        if reflection.water_intake_glasses >= 8:
            water_streak, _ = WellnessStreak.objects.get_or_create(
                user=user,
                streak_type='water',
                defaults={'current_streak': 0, 'longest_streak': 0}
            )
            water_streak.update_streak(activity_date)
        
        # Social streak
        if reflection.social_interactions > 0:
            social_streak, _ = WellnessStreak.objects.get_or_create(
                user=user,
                streak_type='social',
                defaults={'current_streak': 0, 'longest_streak': 0}
            )
            social_streak.update_streak(activity_date)
    
    except Reflection.DoesNotExist:
        pass

def get_recent_user_data(user):
    """Get recent user data for context in forms"""
    recent_reflections = Reflection.objects.filter(user=user).order_by('-date')[:3]
    
    return {
        'recent_mood': [r.mood_rating for r in recent_reflections],
        'recent_anxiety': [r.anxiety_level for r in recent_reflections],
        'recent_stress': [r.stress_level for r in recent_reflections],
        'last_exercise': recent_reflections[0].exercise_minutes if recent_reflections else 0,
        'last_social': recent_reflections[0].social_interactions if recent_reflections else 0,
        'last_water': recent_reflections[0].water_intake_glasses if recent_reflections else 0
    }

def get_goal_progress(goal):
    """Get detailed progress data for a goal"""
    if goal.frequency == 'daily':
        days = 7
    elif goal.frequency == 'weekly':
        days = 30
    else:
        days = 90
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get relevant reflections for goal tracking
    reflections = Reflection.objects.filter(
        user=goal.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    progress_data = {
        'dates': [],
        'values': [],
        'target': float(goal.target_value) if goal.target_value else 0
    }
    
    for reflection in reflections:
        progress_data['dates'].append(reflection.date.strftime('%m/%d'))
        
        # Calculate value based on goal type
        if goal.goal_type == 'exercise':
            value = reflection.exercise_minutes
        elif goal.goal_type == 'social':
            value = reflection.social_interactions
        elif goal.goal_type == 'water':
            value = reflection.water_intake_glasses
        else:
            value = 0
        
        progress_data['values'].append(value)
    
    return progress_data

def generate_insights(user):
    """Generate personalized insights based on user data"""
    insights = []
    
    # Get recent data
    recent_reflections = Reflection.objects.filter(
        user=user,
        date__gte=timezone.now().date() - timedelta(days=7)
    )
    
    if not recent_reflections:
        insights.append("Start tracking your daily reflections to get personalized insights!")
        return insights
    
    # Analyze mood trends
    avg_mood = recent_reflections.aggregate(Avg('mood_rating'))['mood_rating__avg']
    if avg_mood and avg_mood < 3:
        insights.append("Your mood has been lower than usual. Consider reaching out to friends or trying a new activity.")
    
    # Analyze exercise patterns
    total_exercise = sum(r.exercise_minutes for r in recent_reflections)
    if total_exercise < 150:  # Less than 30 min/day average
        insights.append("You might benefit from more physical activity. Even 10 minutes of walking can help!")
    
    # Analyze social patterns
    total_social = sum(r.social_interactions for r in recent_reflections)
    if total_social < 5:
        insights.append("Social connections are important for mental health. Consider reaching out to someone today.")
    
    # Analyze sleep patterns
    sleep_data = [r.sleep_hours for r in recent_reflections if r.sleep_hours]
    if sleep_data:
        avg_sleep = sum(sleep_data) / len(sleep_data)
        if avg_sleep < 7:
            insights.append("Getting enough sleep is crucial for mental wellness. Aim for 7-9 hours per night.")
    
    return insights
