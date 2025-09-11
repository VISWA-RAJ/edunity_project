# memes/forms.py
from django import forms
# --- THE FIX IS HERE: Comment has been added to the import ---
from .models import Meme, Comment

class ImageMemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['caption', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class VideoMemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['caption', 'video_link']
        widgets = {
            'video_link': forms.URLInput(attrs={'placeholder': 'Paste Instagram Reel or YouTube Shorts link'})
        }
        labels = {
            'video_link': 'Instagram or YouTube Link'
        }

    def clean_video_link(self):
        link = self.cleaned_data.get('video_link')
        if 'instagram.com/reel/' not in link and 'youtube.com/shorts/' not in link:
            raise forms.ValidationError("Please paste a valid link from Instagram Reels or YouTube Shorts.")
        return link

# --- THIS FORM NOW WORKS BECAUSE Comment IS IMPORTED ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }
        labels = { 'text': '' }