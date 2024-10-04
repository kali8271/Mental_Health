# community/views.py
from django.views.generic import TemplateView

class ForumView(TemplateView):
    template_name = 'community/forum.html'  # Path to your template
