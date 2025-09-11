# notices/forms.py
from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    # These are the options the user will see in the dropdown
    DURATION_CHOICES = [
        ('1_hour', '1 Hour'),
        ('1_day', '1 Day'),
        ('7_days', '7 Days'),
        ('never', 'Permanent (Never Expires)'),
    ]

    # This is a new field that is ONLY in the form, not the model.
    # We will use it to calculate the expiry_date.
    expiry_duration = forms.ChoiceField(choices=DURATION_CHOICES, required=True, label="Show this notice for")

    class Meta:
        model = Notice
        fields = ['title', 'content', 'category', 'expiry_duration']