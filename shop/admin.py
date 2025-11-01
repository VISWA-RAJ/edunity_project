from django.contrib import admin
from .models import ShopItem

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id', 'price', 'description')
    search_fields = ('name', 'unique_id')
    
    # This makes the unique_id field read-only after creation
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['unique_id']
        return []
