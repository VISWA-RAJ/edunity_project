# polls/admin.py
from django.contrib import admin
from .models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    """
    This allows us to see and edit Choices directly on the Poll admin page.
    """
    model = Choice
    extra = 2 # Show 2 empty forms for adding new choices
    
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at')
    search_fields = ('question', 'created_by__username')
    date_hierarchy = 'created_at'
    
    # Add the ChoiceInline to the bottom of the Poll detail page
    inlines = [ChoiceInline]