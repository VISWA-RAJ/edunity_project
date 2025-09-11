from django.contrib import admin
from .models import LostItem

# This is the new custom action function
@admin.action(description='Mark selected items as Found')
def mark_as_found(modeladmin, request, queryset):
    """
    This action takes the selected items (the queryset) and updates their
    status field to 'Found'.
    """
    queryset.update(status='Found')

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    # This is the configuration we created before
    list_display = ('item_name', 'reported_by', 'status', 'reported_at')
    list_filter = ('status',)
    search_fields = ('item_name', 'description', 'reported_by__username')
    date_hierarchy = 'reported_at'
    
    # --- THIS IS THE NEW PART ---
    # This line adds our new custom function to the "Action" dropdown menu.
    actions = [mark_as_found]
