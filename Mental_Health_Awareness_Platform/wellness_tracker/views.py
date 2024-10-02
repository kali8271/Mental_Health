from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReflectionForm
from .models import Reflection
from django.utils import timezone

@login_required
def add_reflection(request):
    today = timezone.now().date()
    reflection, created = Reflection.objects.get_or_create(user=request.user, date=today)

    if request.method == 'POST':
        form = ReflectionForm(request.POST, instance=reflection)
        if form.is_valid():
            form.save()
            return redirect('reflection_list')
    else:
        form = ReflectionForm(instance=reflection)

    return render(request, 'tracker/reflection.html', {'form': form})

@login_required
def reflection_list(request):
    reflections = Reflection.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/reflection_list.html', {'reflections': reflections})
