from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

@login_required
def enhanced_dashboard(request):
    """Enhanced dashboard with interactive features and analytics"""
    context = {
        'user': request.user,
        'page_title': 'Enhanced Dashboard'
    }
    return render(request, 'enhanced_dashboard.html', context)

