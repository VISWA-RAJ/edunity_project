# lostandfound/forms.py
from django import forms
from .models import LostItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        # We only want the user to fill out these fields
        fields = ['item_name', 'description', 'image', 'last_known_location', 'contact_info']