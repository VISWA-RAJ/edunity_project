# notices/admin.py
from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'expiry_date')
    list_filter = ('category',)
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    
    # This tells the admin to automatically create a link for the 'author' field
    # to the corresponding User's admin page.
    list_display_links = ('title', 'author')