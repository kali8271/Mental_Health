from django.shortcuts import render, get_object_or_404
from .models import Resource

def resource_list(request):
    resources = Resource.objects.all().order_by('-created_at')
    return render(request, 'resources/resource_list.html', {'resources': resources})

def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    return render(request, 'resources/resource_detail.html', {'resource': resource})
