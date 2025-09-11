from django.contrib import admin
from .models import Meme, Comment

@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Meme model.
    """
    
    # --- 1. What to display in the list of all memes ---
    # This adds new, informative columns to the list view.
    list_display = ('caption', 'author', 'meme_type', 'created_at', 'like_count')

    # --- 2. Add a filter sidebar ---
    # This allows you to quickly see only 'Image' or 'Video' posts.
    list_filter = ('meme_type',)

    # --- 3. Add a powerful search bar ---
    # This lets you search by the caption or the author's username.
    search_fields = ('caption', 'author__username')

    # --- 4. Add date navigation ---
    # This creates a timeline navigation bar at the top of the list.
    date_hierarchy = 'created_at'
    
    # This is a custom method to add the "Like Count" column.
    @admin.display(description='Likes')
    def like_count(self, obj):
        return obj.likes.count()

# We can also register the Comment model to see and manage comments.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'meme', 'created_at')
    search_fields = ('text', 'author__username', 'meme__caption')
