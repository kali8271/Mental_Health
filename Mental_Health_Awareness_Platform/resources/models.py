from django.db import models
from django.conf import settings

class Resource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=20, choices=[('blog', 'Blog'), ('video', 'Video')])
    url = models.URLField(blank=True, null=True)  # For video resources or external links

    def __str__(self):
        return self.title
