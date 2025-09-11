# studymaterials/admin.py
from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'uploaded_at')
    search_fields = ('title', 'description', 'uploader__username')
    date_hierarchy = 'uploaded_at'