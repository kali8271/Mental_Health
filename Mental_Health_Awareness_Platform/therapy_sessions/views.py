from django.shortcuts import render, redirect
from .models import Session
from django.contrib.auth.decorators import login_required

@login_required
def schedule_session(request):
    if request.method == 'POST':
        therapist = request.user if request.user.role == 'therapist' else None
        client = request.user if request.user.role == 'client' else None
        date = request.POST['date']
        time = request.POST['time']
        Session.objects.create(therapist=therapist, client=client, date=date, time=time, status='booked')
        return redirect('session_list')
    return render(request, 'therapy_sessions/schedule.html')

@login_required
def session_list(request):
    if request.user.role == 'therapist':
        sessions = request.user.therapist_sessions.all()
    else:
        sessions = request.user.client_sessions.all()
    return render(request, 'therapy_sessions/session_list.html', {'sessions': sessions})
