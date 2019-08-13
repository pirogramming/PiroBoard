from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'user',
            'image',
        ]


    def clean_username(self):
        pass
        name = self.cleaned_data.get('user.username', '')
        #if name:
        #    if get_user_model().objects.filter(self.user.username=name).exists():
        #        raise forms.ValidationError('중복된 사용자 이름입니다.')
        #return name


    #def clean_image(self):

    #    max_width = max_height = 100
    #    try:
    #
    #else




