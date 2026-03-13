from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Uses Django's built in user creation form
# Building off of it, we can add new custom fields such as email
class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-input'}),
            'email': forms.EmailInput(attrs={'class': 'custom-input'}),
        }


    