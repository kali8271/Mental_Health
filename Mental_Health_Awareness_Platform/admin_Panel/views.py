from django.shortcuts import render

def dashboard(request):
    return render(request, 'admin/dashboard.html')  # Render the admin dashboard template
