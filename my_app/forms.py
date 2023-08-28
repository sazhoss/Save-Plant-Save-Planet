from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'category', 'image']
        widgets = {
            'category': forms.Select(),
            'uploader': forms.Select(),
            'description': forms.Textarea(),
        }

class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(),
    )
    
    class Meta:
         model = User
         fields = ['username', 'email', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
         model = User
         fields = ['username', 'email', 'image']