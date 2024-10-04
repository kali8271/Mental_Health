# community/views.py

from django.shortcuts import render, redirect
from .models import Post
from django.http import HttpResponse

def forum(request):
    posts = Post.objects.all()
    return render(request, 'community/forum.html', {'posts': posts})

def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content)
        return redirect('forum')  # Redirect to forum view
    return render(request, 'community/create_post.html')
