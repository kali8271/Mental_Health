from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.contrib import admin

admin.site.site_header = "Mental Health Awareness Platform Admin"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to the Admin Panel"

from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile, UserAdmin)


