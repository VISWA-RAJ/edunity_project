# polls/forms.py
from django import forms

class PollForm(forms.Form):
    question = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'E.g., Should the fest be extended?'}), label="Poll Question")
    choice1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Option 1 (Required)'}), label="Choice 1")
    choice2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Option 2 (Required)'}), label="Choice 2")
    choice3 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Option 3 (Optional)'}), required=False, label="Choice 3")
    choice4 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Option 4 (Optional)'}), required=False, label="Choice 4")