"""
URL configuration for Mental_Health_Awareness_Platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contact/',contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('sessions/', include('therapy_sessions.urls')),
    path('tracker/', include('wellness_tracker.urls')),
    path('resources/', include('resources.urls')),
    path('payments/', include('payments.urls')),
    path('admin-panel/', include('admin_Panel.urls')),
    path('chat/',include('chat.urls')),
    path('community/', include('community.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
