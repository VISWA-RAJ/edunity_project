# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Please provide a valid email address.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

# --- NEW FORM FOR POINT CONVERSION ---

class PointConversionForm(forms.Form):
    points_to_convert = forms.IntegerField(
        label="Points to Convert",
        min_value=10, # User must convert at least 10 points
        help_text="Converts at a rate of 10 points = 1 token."
    )

    def __init__(self, *args, **kwargs):
        # We pass the user's current points to the form to validate it
        self.max_points = kwargs.pop('max_points', 0)
        super().__init__(*args, **kwargs)
        
        # Set the 'max' attribute on the HTML input for a better user experience
        self.fields['points_to_convert'].widget.attrs['max'] = self.max_points
        self.fields['points_to_convert'].widget.attrs['placeholder'] = f'Max: {self.max_points}'

    def clean_points_to_convert(self):
        points = self.cleaned_data.get('points_to_convert')
        
        if points > self.max_points:
            raise forms.ValidationError(f"You only have {self.max_points} points available to convert.")
        
        if points % 10 != 0:
            raise forms.ValidationError("You must convert points in multiples of 10.")
            
        return points
