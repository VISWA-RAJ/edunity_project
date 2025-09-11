# forum/admin.py
from django.contrib import admin
from .models import Doubt, Reply

class ReplyInline(admin.TabularInline):
    """
    This allows us to see (but not edit) replies directly on the Doubt admin page.
    """
    model = Reply
    extra = 0 # Don't show any empty forms for new replies
    readonly_fields = ('author', 'text', 'created_at') # Make the fields read-only
    can_delete = True # Allow deleting replies from here

@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    # What columns to display in the main list of doubts
    list_display = ('title', 'author', 'created_at', 'reply_count')
    
    # Add a search bar
    search_fields = ('title', 'description', 'author__username')
    
    # Add a date navigation bar
    date_hierarchy = 'created_at'
    
    # This adds the ReplyInline to the bottom of the Doubt detail page
    inlines = [ReplyInline]

    # Custom method to calculate the reply count for the list display
    @admin.display(description='Replies')
    def reply_count(self, obj):
        return obj.replies.count()

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    # A simple admin for managing all replies in one place
    list_display = ('text', 'author', 'doubt', 'created_at', 'total_votes')
    search_fields = ('text', 'author__username', 'doubt__title')