from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.contrib import admin
from django.contrib import admin
from .models import  UserProfile
from experts.models import Expert


admin.site.site_header = "Mental Health Awareness Platform Admin"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to the Admin Panel"

  # Import your models

# Customize the admin display for Expert
# class ExpertAdmin(admin.ModelAdmin):
#     list_display = ('name', 'specialization', 'years_of_experience')
#     search_fields = ('name', 'specialization')
#     list_filter = ('years_of_experience',)

# # Customize the admin display for UserProfile
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'photo', 'created_at')
#     search_fields = ('user__username',)
#     list_filter = ('created_at',)

# # Register your models to appear in the admin interface
# admin.site.register(Expert, ExpertAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)


admin.site.register(UserProfile, UserAdmin)


