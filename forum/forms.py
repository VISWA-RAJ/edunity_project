# forum/forms.py
from django import forms
from .models import Doubt, Reply

class DoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'E.g., What is normalization in DBMS?'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Explain your doubt in detail...'}),
        }
        labels = {
            'image': 'Attach an Image (Optional)'
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }
        labels = { 'text': '' }