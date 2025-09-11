# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, FriendRequest, Notification

# Unregister the original User admin
admin.site.unregister(User)

# Define an inline admin descriptor for the Profile model
# This allows us to edit the Profile on the same page as the User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    
    # Add 'profile_points' to the list of columns displayed on the user list page
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_points')
    
    # Add a search bar
    search_fields = ('username', 'email')

    # This is a custom method to get the points from the related Profile
    @admin.display(ordering='profile__points', description='EDUnity Points')
    def profile_points(self, obj):
        return obj.profile.points

# Re-register User with our custom admin
admin.site.register(User, CustomUserAdmin)

# We can also register our other core models to view them
admin.site.register(FriendRequest)
admin.site.register(Notification)