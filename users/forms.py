from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField()
    region = forms.CharField()
    nickname = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'region', 'nickname', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user', 'group',)
