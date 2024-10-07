from django.shortcuts import render
from experts.models import Expert
def home(request):
    experts = Expert.objects.all()  
    return render(request, 'home.html',{'experts' : experts})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')