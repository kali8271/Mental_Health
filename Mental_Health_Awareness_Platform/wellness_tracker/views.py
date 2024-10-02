from django.shortcuts import render, redirect
from .models import WellnessEntry
from django.contrib.auth.decorators import login_required

@login_required
def wellness_entry(request):
    if request.method == 'POST':
        mood = request.POST['mood']
        reflection = request.POST['reflection']
        WellnessEntry.objects.create(user=request.user, mood=mood, reflection=reflection)
        return redirect('wellness_entries')
    return render(request, 'wellness_tracker/entry.html')

@login_required
def wellness_entries(request):
    entries = WellnessEntry.objects.filter(user=request.user)
    return render(request, 'wellness_tracker/entries.html', {'entries': entries})
