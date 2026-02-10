from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    profile_pic = forms.ImageField()
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'profile_pic', 'password']

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    profile_pic = forms.ImageField()
    address = forms.CharField()
    phone = forms.CharField()
    bio = forms.CharField()
   
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "address", "bio", "phone", "profile_pic"]
