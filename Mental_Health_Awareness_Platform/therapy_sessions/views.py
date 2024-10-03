from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ScheduleSessionForm
from .models import TherapySession

@login_required
def schedule_session(request):
    if request.method == 'POST':
        form = ScheduleSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.client = request.user
            session.booked = True
            session.save()
            return redirect('session_list')
    else:
        form = ScheduleSessionForm()
    return render(request, 'therapy_sesseions/schedule.html', {'form': form})
@login_required
def session_list(request):
    sessions = TherapySession.objects.filter(client=request.user)
    return render(request, 'therapy_sesseions/session_list.html', {'sessions': sessions})
