from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'photo', 'banner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
        }